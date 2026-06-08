#!/usr/bin/env python3
"""Run TOPx Lyme open-data catalog searches from the query CSV.

Outputs are intentionally redundant:
- raw response bodies for reproducibility
- schema-shaped JSON envelopes for future machine ingestion
- per-query Markdown notes for human review
- run-level manifests and logs for debugging
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


SOFTWARE_NAME = "topx-lyme-catalog-explorer"
SOFTWARE_VERSION = "0.1.0"
CSV_NAME = "topx_lyme_search_queries.csv"
DEFAULT_USER_AGENT = "topx-lyme-explorer/0.1"
OMIT_EMPTY_OPTIONAL_PARAMS = {"api_key", "email", "key"}
PRIVATE_KEYS = {
    "DATA_GOV_API_KEY",
    "CENSUS_API_KEY",
    "NOAA_CDO_TOKEN",
    "CDC_SOCRATA_APP_TOKEN",
    "HEALTHDATA_SOCRATA_APP_TOKEN",
    "NCBI_API_KEY",
    "OPENFDA_API_KEY",
}
MOUNTAIN_TIME = ZoneInfo("America/Denver")


@dataclass(frozen=True)
class QueryRow:
    search_id: str
    run_order: int
    priority: str
    research_theme: str
    catalog_name: str
    catalog_slug: str
    source_type: str
    query_mode: str
    http_method: str
    endpoint_template: str
    search_term: str
    search_expression: str | None
    request_parameters: dict[str, Any]
    geography_scope: str
    time_scope: str
    expected_record_type: str
    what_are_we_expecting: str
    downstream_use: str
    auth_requirement: str
    auth_env_var: str | None
    pagination_strategy: str
    rate_limit_note: str
    dedupe_key_hint: str
    join_keys_expected: str
    requires_schema_discovery: bool
    source_docs_url: str
    notes: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def mountain_time_run_id(now: datetime | None = None) -> str:
    """Return a human-readable, Windows-safe Mountain Time run folder name."""
    mt_now = (now or datetime.now(timezone.utc)).astimezone(MOUNTAIN_TIME)
    return mt_now.strftime("%Y-%m-%d_%H-%M-%S_%Z")


def slug_part(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:80] or "query"


def load_dotenv(paths: list[Path]) -> dict[str, str]:
    loaded: dict[str, str] = {}
    for path in paths:
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
            loaded[key] = value
    return loaded


def env_with_defaults() -> dict[str, str]:
    env = dict(os.environ)
    env.setdefault("START_DATE", "2024-05-01")
    env.setdefault("END_DATE", "2024-05-07")
    env.setdefault("NOAA_LOCATION_ID", "FIPS:24")
    env.setdefault("WONDER_DATABASE_ID", "nndss_annual")
    env.setdefault("WONDER_REQUEST_XML_FILE", "")
    env.setdefault("WONDER_REQUEST_XML", "")
    return env


def read_wonder_xml(env: dict[str, str]) -> str:
    xml_text = env.get("WONDER_REQUEST_XML", "").strip()
    xml_file = env.get("WONDER_REQUEST_XML_FILE", "").strip()
    if xml_file:
        path = Path(xml_file)
        if path.exists():
            xml_text = path.read_text(encoding="utf-8-sig")
    return xml_text


def xml_parameters(root: ET.Element) -> dict[str, str]:
    parameters: dict[str, str] = {}
    for parameter in root.findall(".//parameter"):
        name = parameter.findtext("name")
        value = parameter.findtext("value") or ""
        if name:
            parameters[name] = value
    return parameters


def extract_wonder_dataset_code(xml_text: str) -> str | None:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None
    return xml_parameters(root).get("dataset_code")


def substitute_placeholders(value: Any, env: dict[str, str]) -> Any:
    if isinstance(value, str):
        return Template(value).safe_substitute(env)
    if isinstance(value, list):
        return [substitute_placeholders(item, env) for item in value]
    if isinstance(value, dict):
        return {key: substitute_placeholders(item, env) for key, item in value.items()}
    return value


def remove_empty_optional_params(params: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key, value in params.items():
        if key.startswith("_"):
            continue
        if key in OMIT_EMPTY_OPTIONAL_PARAMS and (value is None or value == "" or str(value).startswith("${")):
            continue
        if value is None or value == "":
            continue
        clean[key] = value
    return clean


def parse_rows(csv_path: Path) -> list[QueryRow]:
    rows: list[QueryRow] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for item in csv.DictReader(handle):
            try:
                params = json.loads(item["request_parameters_json"] or "{}")
            except json.JSONDecodeError as exc:
                raise ValueError(f"{item.get('search_id')}: invalid request_parameters_json: {exc}") from exc
            rows.append(
                QueryRow(
                    search_id=item["search_id"],
                    run_order=int(item["run_order"]),
                    priority=item["priority"],
                    research_theme=item["research_theme"],
                    catalog_name=item["catalog_name"],
                    catalog_slug=item["catalog_slug"],
                    source_type=item["source_type"],
                    query_mode=item["query_mode"],
                    http_method=item["http_method"].upper(),
                    endpoint_template=item["endpoint_template"],
                    search_term=item["search_term"],
                    search_expression=item.get("search_expression") or None,
                    request_parameters=params,
                    geography_scope=item["geography_scope"],
                    time_scope=item["time_scope"],
                    expected_record_type=item["expected_record_type"],
                    what_are_we_expecting=item["what_are_we_expecting"],
                    downstream_use=item["downstream_use"],
                    auth_requirement=normalize_auth_requirement(item["auth_requirement"]),
                    auth_env_var=item.get("auth_env_var") or None,
                    pagination_strategy=item["pagination_strategy"],
                    rate_limit_note=item["rate_limit_note"],
                    dedupe_key_hint=item["dedupe_key_hint"],
                    join_keys_expected=item["join_keys_expected"],
                    requires_schema_discovery=(item["requires_schema_discovery"].lower() == "true"),
                    source_docs_url=item["source_docs_url"],
                    notes=item["notes"],
                )
            )
    return rows


def normalize_auth_requirement(value: str) -> str:
    if value == "account/license caveat":
        return "account_or_license_may_be_required"
    if value == "":
        return "none"
    return value


def filter_rows(rows: list[QueryRow], args: argparse.Namespace) -> list[QueryRow]:
    selected = rows
    if args.catalog:
        wanted = {item.strip() for item in args.catalog.split(",") if item.strip()}
        selected = [row for row in selected if row.catalog_slug in wanted]
    if args.exclude_catalog:
        excluded = {item.strip() for item in args.exclude_catalog.split(",") if item.strip()}
        selected = [row for row in selected if row.catalog_slug not in excluded]
    if args.priority:
        wanted_priority = {item.strip() for item in args.priority.split(",") if item.strip()}
        selected = [row for row in selected if row.priority in wanted_priority]
    if args.query_mode:
        wanted_modes = {item.strip() for item in args.query_mode.split(",") if item.strip()}
        selected = [row for row in selected if row.query_mode in wanted_modes]
    selected = sorted(selected, key=lambda row: row.run_order)
    if args.smoke_test:
        by_catalog: dict[str, QueryRow] = {}
        for row in selected:
            wonder_xml_available = bool(args.wonder_request_xml_file or os.environ.get("WONDER_REQUEST_XML") or os.environ.get("WONDER_REQUEST_XML_FILE"))
            if row.http_method == "POST" and row.catalog_slug == "cdc_wonder" and not wonder_xml_available:
                continue
            if row.catalog_slug not in by_catalog:
                by_catalog[row.catalog_slug] = row
        selected = list(by_catalog.values())
    if args.max_queries:
        selected = selected[: args.max_queries]
    return selected


def build_output_paths(output_dir: Path, run_id: str, row: QueryRow, page_number: int) -> dict[str, Path]:
    query_slug = f"{row.search_id}_{slug_part(row.search_term)}"
    base = output_dir / "runs" / run_id
    catalog_dir = base / "catalogs" / row.catalog_slug / query_slug
    return {
        "base": base,
        "catalog": catalog_dir,
        "raw": catalog_dir / "raw" / f"page_{page_number:04d}",
        "json": catalog_dir / "json" / f"page_{page_number:04d}.json",
        "markdown": catalog_dir / "notes" / "query.md",
    }


def headers_for(row: QueryRow, env: dict[str, str], user_agent: str) -> dict[str, str]:
    headers = {"User-Agent": user_agent, "Accept": "application/json, text/csv;q=0.9, text/html;q=0.8, */*;q=0.5"}
    if row.auth_env_var and env.get(row.auth_env_var):
        if row.catalog_slug == "data_gov":
            headers["X-Api-Key"] = env[row.auth_env_var]
        elif row.auth_env_var in {"CDC_SOCRATA_APP_TOKEN", "HEALTHDATA_SOCRATA_APP_TOKEN"}:
            headers["X-App-Token"] = env[row.auth_env_var]
        elif row.auth_env_var == "NOAA_CDO_TOKEN":
            headers["token"] = env[row.auth_env_var]
    if row.catalog_slug == "cdc_wonder":
        headers["Accept"] = "application/xml, text/xml, */*"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif row.http_method == "POST":
        headers["Content-Type"] = "application/json"
    return headers


def request_for(row: QueryRow, env: dict[str, str], user_agent: str) -> tuple[Request, dict[str, Any], str | bytes | None]:
    endpoint = Template(row.endpoint_template).safe_substitute(env)
    params = remove_empty_optional_params(substitute_placeholders(row.request_parameters, env))
    body: str | bytes | None = None
    if row.catalog_slug == "cdc_wonder":
        xml_text = read_wonder_xml(env)
        if not xml_text:
            raise RuntimeError("CDC WONDER requires WONDER_REQUEST_XML or WONDER_REQUEST_XML_FILE.")
        dataset_code = env.get("WONDER_DATABASE_ID") or extract_wonder_dataset_code(xml_text)
        if dataset_code in {"", "nndss_annual", "${WONDER_DATABASE_ID}", None}:
            dataset_code = extract_wonder_dataset_code(xml_text)
        if not dataset_code:
            raise RuntimeError("CDC WONDER dataset code was not found in env or request XML.")
        url = f"https://wonder.cdc.gov/controller/datarequest/{dataset_code}"
        params = {
            "request_xml": xml_text,
            "accept_datause_restrictions": "true",
            "dataset_code": dataset_code,
        }
        body = urlencode({"request_xml": xml_text, "accept_datause_restrictions": "true"}).encode("utf-8")
        request = Request(url=url, data=body, headers=headers_for(row, env, user_agent), method="POST")
        return request, params, body
    if row.http_method == "GET":
        query = urlencode(params, doseq=True)
        url = endpoint + (("&" if "?" in endpoint else "?") + query if query else "")
    elif row.http_method == "POST":
        url = endpoint
        body = json.dumps(params).encode("utf-8")
    else:
        url = endpoint
    request = Request(url=url, data=body, headers=headers_for(row, env, user_agent), method=row.http_method)
    return request, params, body


def redact_url(url: str) -> str:
    parts = urlsplit(url)
    if not parts.query:
        return url
    redacted_query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        if key.lower() in {"api_key", "key", "token"}:
            redacted_query.append((key, "<redacted>"))
        else:
            redacted_query.append((key, value))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(redacted_query, doseq=True), parts.fragment))


def polite_delay(row: QueryRow, credential_sent: bool, smoke_test: bool) -> float:
    if smoke_test:
        return 0
    if row.catalog_slug in {"pubmed", "pubmed_central"}:
        return 0.12 if credential_sent else 0.4
    if row.catalog_slug == "noaa_cdo":
        return 0.22
    if not credential_sent and row.auth_requirement != "required":
        return 0.35
    return 0.05


def execute_http(request: Request, timeout: int, max_retries: int) -> tuple[int, dict[str, str], bytes, int]:
    attempt = 0
    while True:
        started = time.perf_counter()
        try:
            with urlopen(request, timeout=timeout) as response:
                body = response.read()
                duration_ms = int((time.perf_counter() - started) * 1000)
                return response.status, dict(response.headers.items()), body, duration_ms
        except HTTPError as exc:
            body = exc.read()
            duration_ms = int((time.perf_counter() - started) * 1000)
            if exc.code in {429, 500, 502, 503, 504} and attempt < max_retries:
                retry_after = exc.headers.get("Retry-After")
                sleep_seconds = float(retry_after) if retry_after and retry_after.isdigit() else min(60, 2**attempt)
                time.sleep(sleep_seconds)
                attempt += 1
                continue
            return exc.code, dict(exc.headers.items()), body, duration_ms
        except URLError:
            if attempt < max_retries:
                time.sleep(min(60, 2**attempt))
                attempt += 1
                continue
            raise


def parse_body(headers: dict[str, str], body: bytes) -> Any:
    content_type = headers.get("Content-Type", "")
    text = body.decode("utf-8", errors="replace")
    if "xml" in content_type or text.lstrip().startswith("<?xml"):
        return text
    if "json" in content_type or text.lstrip().startswith(("{", "[")):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    return text


def sha256_bytes(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def write_raw(path_no_suffix: Path, headers: dict[str, str], body: bytes) -> Path:
    content_type = headers.get("Content-Type", "")
    suffix = ".json" if "json" in content_type else ".xml" if "xml" in content_type else ".csv" if "csv" in content_type else ".html" if "html" in content_type else ".bin"
    path = path_no_suffix.with_suffix(suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    return path


def source_url_for(row: QueryRow, raw: Any, fallback_url: str | None = None) -> str:
    if isinstance(raw, dict):
        for key in ("url", "link", "permalink", "landingPage"):
            value = raw.get(key)
            if isinstance(value, str) and value.startswith("http"):
                return value
        resource = raw.get("resource")
        if isinstance(resource, dict):
            rid = resource.get("id")
            domain = raw.get("metadata", {}).get("domain") if isinstance(raw.get("metadata"), dict) else None
            if rid and domain:
                return f"https://{domain}/d/{rid}"
    if fallback_url and fallback_url.startswith("http"):
        return fallback_url
    return row.endpoint_template if row.endpoint_template.startswith("http") else "https://example.invalid"


def text_value(*values: Any, fallback: str = "") -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (int, float)):
            return str(value)
    return fallback


def record_from_raw(row: QueryRow, raw: Any, index: int, retrieved_at: str, retrieval_url: str, raw_path: str) -> dict[str, Any]:
    source_record_id = text_value(
        raw.get("id") if isinstance(raw, dict) else None,
        raw.get("identifier") if isinstance(raw, dict) else None,
        raw.get("uid") if isinstance(raw, dict) else None,
        raw.get("nctId") if isinstance(raw, dict) else None,
        fallback=f"{row.search_id}-{index}",
    )
    title = text_value(
        raw.get("title") if isinstance(raw, dict) else None,
        raw.get("name") if isinstance(raw, dict) else None,
        raw.get("briefTitle") if isinstance(raw, dict) else None,
        raw.get("resource", {}).get("name") if isinstance(raw, dict) and isinstance(raw.get("resource"), dict) else None,
        fallback=row.search_term,
    )
    description = text_value(
        raw.get("description") if isinstance(raw, dict) else None,
        raw.get("abstract") if isinstance(raw, dict) else None,
        raw.get("resource", {}).get("description") if isinstance(raw, dict) and isinstance(raw.get("resource"), dict) else None,
        fallback="",
    ) or None
    publisher = text_value(
        raw.get("publisher") if isinstance(raw, dict) else None,
        raw.get("organization") if isinstance(raw, dict) else None,
        raw.get("resource", {}).get("attribution") if isinstance(raw, dict) and isinstance(raw.get("resource"), dict) else None,
        fallback="",
    ) or None
    raw_serialized = json.dumps(raw, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    return {
        "normalized_id": f"{row.catalog_slug}:{source_record_id}",
        "source_record_id": source_record_id,
        "record_type": row.expected_record_type or row.query_mode,
        "title": title,
        "description": description,
        "summary": None,
        "source_url": source_url_for(row, raw, retrieval_url),
        "retrieved_at": retrieved_at,
        "modified_at": None,
        "issued_at": None,
        "publisher": publisher,
        "organizations": [{"name": publisher, "role": "publisher", "identifier": None, "url": None}] if publisher else [],
        "people": [],
        "identifiers": identifiers_for(row, raw, source_record_id),
        "topics": [],
        "conditions": [row.search_term] if row.research_theme in {"disease_core", "diagnosis_testing"} else [],
        "pathogens": [],
        "vectors": [],
        "interventions": [],
        "medications": [row.search_term] if row.research_theme == "treatment" else [],
        "geographies": [{"level": "national", "name": row.geography_scope or "United States"}],
        "temporal_coverage": {"start_date": None, "end_date": None, "years": [], "vintage": row.time_scope, "update_frequency": None},
        "access": {
            "access_level": "public" if row.auth_requirement != "account_or_license_may_be_required" else "restricted_public",
            "machine_readable": True,
            "api_available": row.query_mode not in {"download_manifest", "full_download"},
            "download_available": row.query_mode in {"download_manifest", "full_download"},
            "requires_account": row.auth_requirement == "required",
            "requires_license": row.auth_requirement == "account_or_license_may_be_required",
            "cost": "free/unknown",
            "license_url": None,
            "rights_notes": row.notes or None,
        },
        "distributions": [],
        "relationships": [],
        "data_quality": {
            "completeness_score": None,
            "freshness_score": None,
            "has_documentation": bool(row.source_docs_url),
            "has_data_dictionary": None,
            "known_limitations": [row.notes] if row.notes else [],
            "suppression_rules": [],
            "manual_review_required": row.requires_schema_discovery,
        },
        "provenance": {
            "source_catalog": row.catalog_slug,
            "search_id": row.search_id,
            "normalization_version": SOFTWARE_VERSION,
            "source_page": 1,
            "source_row_index": index,
            "retrieval_url": retrieval_url,
            "raw_file_path": raw_path,
            "raw_record_sha256": sha256_bytes(raw_serialized),
        },
        "raw_metadata": raw if isinstance(raw, dict) else {"value": raw},
    }


def identifiers_for(row: QueryRow, raw: Any, source_record_id: str) -> dict[str, str | int | float | None]:
    identifiers: dict[str, str | int | float | None] = {}
    if row.catalog_slug.startswith("pubmed"):
        identifiers["pmid" if row.catalog_slug == "pubmed" else "pmcid"] = source_record_id
    elif row.catalog_slug == "clinicaltrials_gov":
        identifiers["nct_id"] = source_record_id
    elif row.catalog_slug == "nih_reporter":
        identifiers["project_number"] = source_record_id
    elif row.catalog_slug == "rxnorm":
        identifiers["rxcui"] = source_record_id
    else:
        identifiers["source_id"] = source_record_id
    if isinstance(raw, dict):
        for key in ("doi", "pmid", "pmcid", "nct_id", "project_number", "rxcui"):
            if key in raw:
                identifiers[key] = raw[key]
    return identifiers


def extract_record_items(row: QueryRow, parsed: Any) -> tuple[list[Any], int | None, bool]:
    if row.catalog_slug == "cdc_wonder" and isinstance(parsed, str):
        records = parse_wonder_records(parsed)
        return records, len(records), False
    if isinstance(parsed, dict):
        if isinstance(parsed.get("results"), list):
            total = parsed.get("resultSetSize") or parsed.get("metadata", {}).get("total") if isinstance(parsed.get("metadata"), dict) else None
            return parsed["results"], int(total) if isinstance(total, int) else None, False
        if isinstance(parsed.get("data"), dict) and isinstance(parsed["data"].get("results"), list):
            meta = parsed["data"].get("metadata", {})
            total = meta.get("resultset", {}).get("count") if isinstance(meta, dict) and isinstance(meta.get("resultset"), dict) else None
            return parsed["data"]["results"], int(total) if isinstance(total, int) else None, False
        if isinstance(parsed.get("studies"), list):
            return parsed["studies"], parsed.get("totalCount"), bool(parsed.get("nextPageToken"))
        if isinstance(parsed.get("esearchresult"), dict):
            ids = parsed["esearchresult"].get("idlist", [])
            total = parsed["esearchresult"].get("count")
            return [{"id": item, "title": item} for item in ids], int(total) if str(total).isdigit() else None, False
        if isinstance(parsed.get("results"), dict):
            return [parsed["results"]], None, False
        if isinstance(parsed.get("results"), list):
            return parsed["results"], None, False
        if isinstance(parsed.get("items"), list):
            return parsed["items"], None, False
        if row.catalog_slug == "nih_reporter" and isinstance(parsed.get("results"), list):
            return parsed["results"], parsed.get("meta", {}).get("total"), False
        return [parsed], None, False
    if isinstance(parsed, list):
        if row.catalog_slug == "census_acs5" and parsed and isinstance(parsed[0], list):
            header = parsed[0]
            records = [dict(zip(header, item)) for item in parsed[1:]]
            return records, len(records), False
        return parsed, len(parsed), False
    return [], None, False


def parse_wonder_records(xml_text: str) -> list[dict[str, Any]]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    dataset = root.find(".//dataset")
    dataset_code = dataset.attrib.get("code") if dataset is not None else None
    dataset_label = dataset.attrib.get("label") if dataset is not None else None
    variable_labels: dict[str, str] = {}
    for variable in root.findall(".//variable"):
        code = variable.attrib.get("code")
        label = variable.attrib.get("label")
        if code and label:
            variable_labels[code] = label
    by_vars = []
    for key, value in xml_parameters(root).items():
        if key.startswith("B_") and value != "*None*":
            by_vars.append(variable_labels.get(value, value))
    records: list[dict[str, Any]] = []
    for row_index, table_row in enumerate(root.findall(".//data-table/r")):
        cells = []
        for cell in table_row.findall("c"):
            cell_value = cell.attrib.get("l") or cell.attrib.get("v") or cell.attrib.get("dt") or cell.text or ""
            cells.append(cell_value)
        if not cells or all(not item for item in cells):
            continue
        fields: dict[str, Any] = {}
        for index, value in enumerate(cells):
            key = by_vars[index] if index < len(by_vars) else f"measure_{index - len(by_vars) + 1}"
            fields[key] = value
        records.append(
            {
                "id": f"{dataset_code or 'wonder'}-{row_index}",
                "title": " | ".join(cells[: max(1, min(len(cells), 3))]),
                "dataset_code": dataset_code,
                "dataset_label": dataset_label,
                "fields": fields,
                "cells": cells,
            }
        )
    return records


def response_rate_limit(headers: dict[str, str]) -> dict[str, Any] | None:
    limit = headers.get("X-RateLimit-Limit") or headers.get("RateLimit-Limit")
    remaining = headers.get("X-RateLimit-Remaining") or headers.get("RateLimit-Remaining")
    if not limit and not remaining:
        return None
    return {
        "limit": int(limit) if limit and limit.isdigit() else None,
        "remaining": int(remaining) if remaining and remaining.isdigit() else None,
        "reset_at": None,
    }


def write_markdown(path: Path, row: QueryRow, envelope: dict[str, Any], retrieval_url: str, raw_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    credential_alias = envelope["query"]["auth"]["credential_alias"] or "none"
    credential_sent = "yes" if envelope["query"]["auth"]["credential_sent"] else "no"
    lines = [
        f"# {row.search_id}: {row.search_term}",
        "",
        f"- Catalog: {row.catalog_name} (`{row.catalog_slug}`)",
        f"- Query mode: `{row.query_mode}`",
        f"- Priority/theme: `{row.priority}` / `{row.research_theme}`",
        f"- Endpoint: `{row.http_method} {row.endpoint_template}`",
        f"- Retrieval URL: `{retrieval_url}`",
        f"- Auth alias: `{credential_alias}`; credential sent: {credential_sent}",
        f"- HTTP status: `{envelope['response']['http_status']}`",
        f"- Records normalized from this page: `{envelope['response']['record_count']}`",
        f"- Raw response: `{raw_path}`",
        f"- JSON envelope: `{path.parent.parent / 'json' / 'page_0001.json'}`",
        "",
        "## Search Intent",
        "",
        row.what_are_we_expecting,
        "",
        "## Downstream Use",
        "",
        row.downstream_use,
        "",
        "## Pagination And Rate Notes",
        "",
        f"- Pagination: {row.pagination_strategy}",
        f"- Rate limit note: {row.rate_limit_note}",
        "",
        "## Interpretation Notes",
        "",
        row.notes or "No row-specific notes.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def process_row(row: QueryRow, args: argparse.Namespace, run_id: str, started_at: str, output_dir: Path, env: dict[str, str]) -> dict[str, Any]:
    page_number = 1
    paths = build_output_paths(output_dir, run_id, row, page_number)
    paths["catalog"].mkdir(parents=True, exist_ok=True)
    retrieved_at = utc_now()
    credential_sent = bool(row.auth_env_var and env.get(row.auth_env_var))
    errors: list[dict[str, Any]] = []
    warnings: list[str] = []
    if row.auth_requirement == "required" and not credential_sent:
        raise RuntimeError(f"{row.search_id}: missing required credential alias {row.auth_env_var}")
    if row.auth_requirement == "optional_recommended" and not credential_sent:
        warnings.append(f"Optional credential {row.auth_env_var} was not found; request used anonymous/public access.")

    request, params, _body = request_for(row, env, args.user_agent)
    safe_url = redact_url(request.full_url)
    logging.info("Running %s %s catalog=%s auth_alias=%s credential_sent=%s", row.search_id, safe_url, row.catalog_slug, row.auth_env_var, credential_sent)
    time.sleep(polite_delay(row, credential_sent, args.smoke_test))
    status, headers, body, duration_ms = execute_http(request, args.timeout, args.max_retries)
    raw_path = write_raw(paths["raw"], headers, body)
    parsed = parse_body(headers, body)
    record_items, total_count, has_more = extract_record_items(row, parsed)
    records = [
        record_from_raw(row, item, index, retrieved_at, safe_url, str(raw_path.relative_to(output_dir)))
        for index, item in enumerate(record_items[: args.max_records_per_page])
    ]
    if status >= 400:
        message = body.decode("utf-8", errors="replace")[:1000]
        errors.append({"error_type": "http_error", "message": message, "retryable": status in {429, 500, 502, 503, 504}, "http_status": status, "details": None})

    raw_hash = sha256_bytes(body)
    envelope: dict[str, Any] = {
        "schema_version": "1.0.0",
        "run": {
            "run_id": run_id,
            "started_at": started_at,
            "completed_at": utc_now(),
            "status": "failed" if errors else "succeeded",
            "software": {"name": SOFTWARE_NAME, "version": SOFTWARE_VERSION, "git_commit": git_commit()},
            "environment": {
                "mode": "smoke_test" if args.smoke_test else "search",
                "credential_aliases_available": ",".join(sorted(k for k in PRIVATE_KEYS if env.get(k))),
            },
        },
        "query": {
            "search_id": row.search_id,
            "query_mode": row.query_mode,
            "method": row.http_method,
            "endpoint": row.endpoint_template,
            "search_term": row.search_term,
            "search_expression": row.search_expression,
            "parameters": redact_params(params),
            "request_body": None,
            "auth": {"requirement": row.auth_requirement, "credential_alias": row.auth_env_var, "credential_sent": credential_sent},
        },
        "source": {
            "catalog_name": row.catalog_name,
            "catalog_slug": row.catalog_slug,
            "source_type": row.source_type,
            "organization": infer_organization(row),
            "docs_url": row.source_docs_url if row.source_docs_url.startswith("http") else "https://example.invalid",
            "license_url": None,
            "terms_url": None,
            "data_use_restrictions": [row.notes] if row.notes else [],
        },
        "response": {
            "retrieved_at": retrieved_at,
            "http_status": status,
            "content_type": headers.get("Content-Type"),
            "duration_ms": duration_ms,
            "request_id": headers.get("X-Request-Id") or headers.get("X-Amzn-Trace-Id"),
            "page": {"page_number": page_number, "page_size": len(record_items), "cursor_in": None, "cursor_out": None, "offset": params.get("offset") or params.get("$offset"), "has_more": has_more},
            "record_count": len(records),
            "total_count": total_count,
            "rate_limit": response_rate_limit(headers),
            "raw_file": {"path": str(raw_path.relative_to(output_dir)), "sha256": raw_hash, "byte_count": len(body)},
        },
        "records": records,
        "warnings": warnings,
        "errors": errors,
    }
    paths["json"].parent.mkdir(parents=True, exist_ok=True)
    paths["json"].write_text(json.dumps(envelope, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    write_markdown(paths["markdown"], row, envelope, safe_url, raw_path)
    return {
        "search_id": row.search_id,
        "catalog_slug": row.catalog_slug,
        "catalog_name": row.catalog_name,
        "status": envelope["run"]["status"],
        "http_status": status,
        "record_count": len(records),
        "total_count": total_count,
        "duration_ms": duration_ms,
        "json_path": str(paths["json"].relative_to(output_dir)),
        "markdown_path": str(paths["markdown"].relative_to(output_dir)),
        "raw_path": str(raw_path.relative_to(output_dir)),
        "warnings": warnings,
        "errors": errors,
    }


def redact_params(params: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in params.items():
        if key.lower() in {"api_key", "key", "token", "request_xml"}:
            redacted[key] = "<redacted>"
        else:
            redacted[key] = value
    return redacted


def infer_organization(row: QueryRow) -> str:
    if "CDC" in row.catalog_name:
        return "Centers for Disease Control and Prevention"
    if "Census" in row.catalog_name:
        return "U.S. Census Bureau"
    if "NOAA" in row.catalog_name:
        return "NOAA National Centers for Environmental Information"
    if "Data.gov" in row.catalog_name:
        return "U.S. General Services Administration"
    if "HealthData" in row.catalog_name:
        return "U.S. Department of Health and Human Services"
    if "ClinicalTrials" in row.catalog_name or "NCBI" in row.catalog_name or "RxNorm" in row.catalog_name:
        return "National Institutes of Health"
    if "FDA" in row.catalog_name:
        return "U.S. Food and Drug Administration"
    return row.catalog_name


def git_commit() -> str | None:
    try:
        import subprocess

        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=Path(__file__).resolve().parents[2], capture_output=True, text=True, timeout=5)
        return result.stdout.strip() or None if result.returncode == 0 else None
    except Exception:
        return None


def write_run_manifest(base: Path, run_id: str, started_at: str, completed_at: str, results: list[dict[str, Any]], args: argparse.Namespace, loaded_env_paths: list[str]) -> None:
    manifest = {
        "run_id": run_id,
        "started_at": started_at,
        "completed_at": completed_at,
        "mode": "smoke_test" if args.smoke_test else "search",
        "query_count": len(results),
        "succeeded": sum(1 for item in results if item["status"] == "succeeded"),
        "failed": sum(1 for item in results if item["status"] == "failed"),
        "partial": sum(1 for item in results if item["status"] == "partial"),
        "loaded_env_paths": loaded_env_paths,
        "catalogs": sorted({item["catalog_slug"] for item in results}),
        "results": results,
    }
    base.mkdir(parents=True, exist_ok=True)
    (base / "run_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    summary_path = base / "search_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["search_id", "catalog_slug", "status", "http_status", "record_count", "total_count", "duration_ms", "json_path", "markdown_path", "raw_path"])
        writer.writeheader()
        for item in results:
            writer.writerow({key: item.get(key) for key in writer.fieldnames})
    errors_path = base / "errors.jsonl"
    with errors_path.open("w", encoding="utf-8") as handle:
        for item in results:
            for error in item.get("errors", []):
                handle.write(json.dumps({"search_id": item["search_id"], "catalog_slug": item["catalog_slug"], **error}, ensure_ascii=False) + "\n")


def setup_logging(base: Path) -> Path:
    logs_dir = base / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "catalog_explorer.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler(sys.stdout)],
    )
    return log_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TOPx Lyme open-data catalog searches.")
    parser.add_argument("--csv", type=Path, default=Path(CSV_NAME), help="Path to topx_lyme_search_queries.csv.")
    parser.add_argument("--env-file", type=Path, action="append", help="Optional .env path. Can be provided more than once.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory. Defaults to TOPX_OUTPUT_DIR or output.")
    parser.add_argument("--smoke-test", action="store_true", help="Run one representative query per selected catalog.")
    parser.add_argument("--catalog", help="Comma-separated catalog_slug filter, e.g. data_gov,census_acs5,noaa_cdo.")
    parser.add_argument("--exclude-catalog", help="Comma-separated catalog_slug values to skip, e.g. cdc_wonder.")
    parser.add_argument("--priority", help="Comma-separated priority filter, e.g. P0,P1.")
    parser.add_argument("--query-mode", help="Comma-separated query_mode filter.")
    parser.add_argument("--max-queries", type=int, help="Stop after N selected queries.")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers. Keep low for public APIs.")
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "60")))
    parser.add_argument("--max-retries", type=int, default=int(os.environ.get("MAX_RETRIES", "5")))
    parser.add_argument("--max-records-per-page", type=int, default=100, help="Limit normalized records per response page.")
    parser.add_argument("--user-agent", default=os.environ.get("TOPX_USER_AGENT", DEFAULT_USER_AGENT))
    parser.add_argument("--wonder-request-xml-file", type=Path, help="CDC WONDER request XML file exported from API Options.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    kit_dir = Path.cwd()
    if not args.csv.is_absolute():
        args.csv = kit_dir / args.csv
    default_env_paths = [kit_dir / ".env", kit_dir.parent / ".env"]
    env_paths = args.env_file or default_env_paths
    loaded = load_dotenv(env_paths)
    env = env_with_defaults()
    if args.wonder_request_xml_file:
        env["WONDER_REQUEST_XML_FILE"] = str(args.wonder_request_xml_file)
    output_dir = args.output_dir or Path(env.get("TOPX_OUTPUT_DIR", "output"))
    if not output_dir.is_absolute():
        output_dir = kit_dir / output_dir
    run_id = mountain_time_run_id()
    started_at = utc_now()
    run_base = output_dir / "runs" / run_id
    log_path = setup_logging(run_base)
    logging.info("Starting run_id=%s smoke_test=%s csv=%s output_dir=%s log=%s", run_id, args.smoke_test, args.csv, output_dir, log_path)
    loaded_env_paths = [str(path) for path in env_paths if path.exists()]
    logging.info("Loaded env files: %s", ", ".join(loaded_env_paths) or "none")
    logging.info("Loaded env aliases: %s", ", ".join(sorted(k for k, value in loaded.items() if k in PRIVATE_KEYS and value)) or "none")

    rows = parse_rows(args.csv)
    selected = filter_rows(rows, args)
    if not selected:
        logging.error("No queries selected.")
        return 2
    if args.smoke_test:
        args.workers = min(args.workers, 4)
    logging.info("Selected %d queries across %d catalogs.", len(selected), len({row.catalog_slug for row in selected}))

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        future_to_row = {executor.submit(process_row, row, args, run_id, started_at, output_dir, env): row for row in selected}
        for future in as_completed(future_to_row):
            row = future_to_row[future]
            try:
                result = future.result()
                results.append(result)
                logging.info("Finished %s status=%s http=%s records=%s", row.search_id, result["status"], result["http_status"], result["record_count"])
            except Exception as exc:
                logging.exception("Failed %s: %s", row.search_id, exc)
                results.append(
                    {
                        "search_id": row.search_id,
                        "catalog_slug": row.catalog_slug,
                        "catalog_name": row.catalog_name,
                        "status": "failed",
                        "http_status": None,
                        "record_count": 0,
                        "total_count": None,
                        "duration_ms": None,
                        "json_path": None,
                        "markdown_path": None,
                        "raw_path": None,
                        "warnings": [],
                        "errors": [{"error_type": type(exc).__name__, "message": str(exc), "retryable": False, "http_status": None, "details": None}],
                    }
                )
    results = sorted(results, key=lambda item: item["search_id"])
    completed_at = utc_now()
    write_run_manifest(run_base, run_id, started_at, completed_at, results, args, loaded_env_paths)
    failures = [item for item in results if item["status"] == "failed"]
    logging.info("Completed run_id=%s succeeded=%d failed=%d manifest=%s", run_id, len(results) - len(failures), len(failures), run_base / "run_manifest.json")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
