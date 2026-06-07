"""
sync_notion.py

One-way sync from local GitHub markdown repo -> Notion Repo Pages database.

Syncs:
- README.md
- wiki/**/*.md
- research/**/*.md
- findings/**/*.md
- prompts/**/*.md

Run:
    pip install requests python-dotenv
    python scripts/sync_notion.py
"""

from __future__ import annotations

import hashlib
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"

SYNC_PATTERNS = [
    "README.md",
    "wiki/**/*.md",
    "research/**/*.md",
    "findings/**/*.md",
    "prompts/**/*.md",
]

MAX_CODE_CHARS = 1800
MAX_BLOCKS_PER_APPEND = 100


class NotionApiError(RuntimeError):
    def __init__(
        self,
        method: str,
        path: str,
        status_code: int,
        response_text: str,
        code: str | None = None,
        message: str | None = None,
    ) -> None:
        self.method = method
        self.path = path
        self.status_code = status_code
        self.response_text = response_text
        self.code = code
        self.message = message
        detail = message or response_text
        super().__init__(f"{method} {path} failed: {status_code}\n{detail}")


class NotionClient:
    def __init__(self, token: str) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            }
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.session.get(f"{BASE_URL}{path}", params=params, timeout=30)
        self._raise_for_error(response, "GET", path)
        return response.json()

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(f"{BASE_URL}{path}", json=payload, timeout=30)
        self._raise_for_error(response, "POST", path)
        return response.json()

    def patch(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.patch(f"{BASE_URL}{path}", json=payload, timeout=30)
        self._raise_for_error(response, "PATCH", path)
        return response.json()

    @staticmethod
    def _raise_for_error(response: requests.Response, method: str, path: str) -> None:
        if not response.ok:
            error_code = None
            error_message = None
            try:
                error_payload = response.json()
                error_code = error_payload.get("code")
                error_message = error_payload.get("message")
            except ValueError:
                pass

            raise NotionApiError(
                method=method,
                path=path,
                status_code=response.status_code,
                response_text=response.text,
                code=error_code,
                message=error_message,
            )

    def query_page_by_repo_path(
        self, database_id: str, repo_path: str
    ) -> dict[str, Any] | None:
        payload = {
            "filter": {
                "property": "Repo Path",
                "rich_text": {"equals": repo_path},
            },
            "page_size": 1,
        }

        result = self.post(f"/databases/{database_id}/query", payload)
        results = result.get("results", [])

        if not results:
            return None

        return results[0]

    def create_repo_page(
        self,
        database_id: str,
        name: str,
        repo_path: str,
        category: str,
        content_hash: str,
        github_url: str | None,
        children: list[dict[str, Any]],
    ) -> str:
        payload = {
            "parent": {"database_id": database_id},
            "properties": build_properties(
                name=name,
                repo_path=repo_path,
                category=category,
                content_hash=content_hash,
                github_url=github_url,
            ),
            "children": children[:MAX_BLOCKS_PER_APPEND],
        }

        result = self.post("/pages", payload)
        page_id = result["id"]

        remaining = children[MAX_BLOCKS_PER_APPEND:]
        if remaining:
            self.append_children(page_id, remaining)

        return page_id

    def update_repo_page(
        self,
        page_id: str,
        name: str,
        repo_path: str,
        category: str,
        content_hash: str,
        github_url: str | None,
        children: list[dict[str, Any]],
    ) -> None:
        self.patch(
            f"/pages/{page_id}",
            {
                "properties": build_properties(
                    name=name,
                    repo_path=repo_path,
                    category=category,
                    content_hash=content_hash,
                    github_url=github_url,
                )
            },
        )

        self.archive_existing_children(page_id)
        self.append_children(page_id, children)

    def append_children(self, page_id: str, children: list[dict[str, Any]]) -> None:
        for start in range(0, len(children), MAX_BLOCKS_PER_APPEND):
            chunk = children[start : start + MAX_BLOCKS_PER_APPEND]
            self.patch(f"/blocks/{page_id}/children", {"children": chunk})

    def archive_existing_children(self, page_id: str) -> None:
        next_cursor: str | None = None

        while True:
            params: dict[str, Any] = {"page_size": 100}
            if next_cursor:
                params["start_cursor"] = next_cursor

            result = self.get(f"/blocks/{page_id}/children", params=params)

            for block in result.get("results", []):
                block_id = block["id"]
                self.patch(f"/blocks/{block_id}", {"archived": True})

            if not result.get("has_more"):
                break

            next_cursor = result.get("next_cursor")


def build_properties(
    name: str,
    repo_path: str,
    category: str,
    content_hash: str,
    github_url: str | None,
) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "Name": {"title": [{"text": {"content": name}}]},
        "Repo Path": {"rich_text": [{"text": {"content": repo_path}}]},
        "Category": {"select": {"name": category}},
        "Last Synced": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
        "Content Hash": {"rich_text": [{"text": {"content": content_hash}}]},
        "Status": {"select": {"name": "Active"}},
    }

    if github_url:
        properties["GitHub URL"] = {"url": github_url}

    return properties


def get_existing_hash(page: dict[str, Any]) -> str | None:
    prop = page.get("properties", {}).get("Content Hash", {})
    rich_text = prop.get("rich_text", [])

    if not rich_text:
        return None

    return rich_text[0].get("plain_text")


def paragraph(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
        },
    }


def heading(text: str, level: int = 2) -> dict[str, Any]:
    block_type = f"heading_{level}"

    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
        },
    }


def code_block(text: str, language: str = "markdown") -> dict[str, Any]:
    return {
        "object": "block",
        "type": "code",
        "code": {
            "language": language,
            "rich_text": [{"type": "text", "text": {"content": text}}],
        },
    }


def chunk_text(text: str, max_chars: int = MAX_CODE_CHARS) -> list[str]:
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


def build_page_blocks(
    repo_path: str, content_hash: str, markdown: str
) -> list[dict[str, Any]]:
    blocks = [
        heading("Synced from GitHub Markdown", 2),
        paragraph(f"Repo path: {repo_path}"),
        paragraph(f"Content hash: {content_hash}"),
        paragraph(
            "This page is generated from the GitHub repo. Edit the markdown file, not this Notion page."
        ),
        heading("Markdown Content", 2),
    ]

    for chunk in chunk_text(markdown):
        blocks.append(code_block(chunk))

    return blocks


def calculate_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def infer_category(repo_path: str) -> str:
    if repo_path == "README.md":
        return "readme"

    first_part = repo_path.split("/", maxsplit=1)[0]

    if first_part in {"wiki", "research", "findings", "prompts"}:
        return first_part

    return "research"


def build_github_url(repo_path: str) -> str | None:
    repository = os.getenv("GITHUB_REPOSITORY")
    branch = os.getenv("GITHUB_DEFAULT_BRANCH", "main")

    if not repository:
        return None

    return f"https://github.com/{repository}/blob/{branch}/{repo_path}"


def find_markdown_files(repo_root: Path) -> list[Path]:
    files: set[Path] = set()

    for pattern in SYNC_PATTERNS:
        for path in repo_root.glob(pattern):
            if path.is_file():
                files.add(path)

    return sorted(files)


def print_notion_error(error: NotionApiError, database_id: str) -> None:
    print(
        f"Notion API error: {error.method} {error.path} failed with "
        f"{error.status_code}.",
        file=sys.stderr,
    )

    if error.code:
        print(f"Code: {error.code}", file=sys.stderr)

    if error.message:
        print(f"Message: {error.message}", file=sys.stderr)

    if error.status_code == 404 and error.code == "object_not_found":
        print(
            "\nThe Notion integration cannot access the Repo Pages database.",
            file=sys.stderr,
        )
        print(f"Configured database ID: {database_id}", file=sys.stderr)
        print(
            "In Notion, open the TopX Lyme Challenge Hub or Repo Pages database, "
            "use Share/Connections, and add the integration tied to NOTION_TOKEN.",
            file=sys.stderr,
        )
        print(
            "Also confirm NOTION_REPO_PAGES_DATABASE_ID matches the Repo Pages database.",
            file=sys.stderr,
        )


def main() -> int:
    load_dotenv()

    token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_REPO_PAGES_DATABASE_ID")

    if not token:
        print("Missing NOTION_TOKEN in .env", file=sys.stderr)
        return 1

    if not database_id:
        print("Missing NOTION_REPO_PAGES_DATABASE_ID in .env", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parents[1]
    markdown_files = find_markdown_files(repo_root)

    if not markdown_files:
        print("No markdown files found to sync.")
        return 0

    client = NotionClient(token)

    try:
        client.get(f"/databases/{database_id}")
    except NotionApiError as error:
        print_notion_error(error, database_id)
        return 1

    print(f"Repo root: {repo_root}")
    print(f"Markdown files found: {len(markdown_files)}")

    created = 0
    updated = 0
    skipped = 0

    for file_path in markdown_files:
        repo_path = file_path.relative_to(repo_root).as_posix()
        markdown = file_path.read_text(encoding="utf-8")
        content_hash = calculate_hash(markdown)
        name = file_path.stem
        category = infer_category(repo_path)
        github_url = build_github_url(repo_path)

        print(f"\nSyncing: {repo_path}")

        existing_page = client.query_page_by_repo_path(database_id, repo_path)

        if existing_page:
            page_id = existing_page["id"]
            existing_hash = get_existing_hash(existing_page)

            if existing_hash == content_hash:
                print("  Skipped. No changes.")
                skipped += 1
                continue

            blocks = build_page_blocks(repo_path, content_hash, markdown)
            client.update_repo_page(
                page_id=page_id,
                name=name,
                repo_path=repo_path,
                category=category,
                content_hash=content_hash,
                github_url=github_url,
                children=blocks,
            )
            print("  Updated.")
            updated += 1

        else:
            blocks = build_page_blocks(repo_path, content_hash, markdown)
            client.create_repo_page(
                database_id=database_id,
                name=name,
                repo_path=repo_path,
                category=category,
                content_hash=content_hash,
                github_url=github_url,
                children=blocks,
            )
            print("  Created.")
            created += 1

    print("\nSync complete.")
    print(f"Created: {created}")
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
