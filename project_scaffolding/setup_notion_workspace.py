"""
setup_notion_workspace.py

Creates a TopX Lyme Challenge workspace inside an existing Notion parent page.

Required .env file in repo root:

NOTION_TOKEN=secret_your_actual_notion_token_here
NOTION_PARENT_PAGE_ID=37847f553235808b8b64fefdb0c70355

Run:
    pip install requests python-dotenv
    python scripts/setup_notion_workspace.py
"""

from __future__ import annotations

import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv

NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"


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

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(f"{BASE_URL}{path}", json=payload, timeout=30)

        if not response.ok:
            raise RuntimeError(
                f"POST {path} failed: {response.status_code}\n{response.text}"
            )

        return response.json()

    def create_page(
        self,
        parent_page_id: str,
        title: str,
        children: list[dict[str, Any]] | None = None,
    ) -> str:
        payload = {
            "parent": {"page_id": parent_page_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}],
                }
            },
            "children": children or [],
        }

        result = self.post("/pages", payload)
        return result["id"]

    def create_database(
        self,
        parent_page_id: str,
        title: str,
        properties: dict[str, Any],
    ) -> str:
        payload = {
            "parent": {"page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties,
        }

        result = self.post("/databases", payload)
        return result["id"]


def paragraph(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
        },
    }


def heading(text: str, level: int = 2) -> dict[str, Any]:
    block_type = f"heading_{level}"

    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": [{"type": "text", "text": {"content": text}}],
        },
    }


def bullet(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
        },
    }


def todo(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "checked": False,
        },
    }


def title_property() -> dict[str, Any]:
    return {"title": {}}


def text_property() -> dict[str, Any]:
    return {"rich_text": {}}


def url_property() -> dict[str, Any]:
    return {"url": {}}


def date_property() -> dict[str, Any]:
    return {"date": {}}


def number_property() -> dict[str, Any]:
    return {"number": {"format": "number"}}


def checkbox_property() -> dict[str, Any]:
    return {"checkbox": {}}


def select_property(options: list[str]) -> dict[str, Any]:
    return {
        "select": {
            "options": [{"name": option} for option in options],
        }
    }


def main() -> int:
    load_dotenv()

    token = os.getenv("NOTION_TOKEN")
    parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")

    if not token:
        print("Missing NOTION_TOKEN in .env", file=sys.stderr)
        return 1

    if not parent_page_id:
        print("Missing NOTION_PARENT_PAGE_ID in .env", file=sys.stderr)
        return 1

    client = NotionClient(token)

    print("Creating TopX Lyme Challenge Hub...")

    hub_id = client.create_page(
        parent_page_id=parent_page_id,
        title="TopX Lyme Challenge Hub",
        children=[
            paragraph(
                "Shared workspace for TopX Lyme Challenge research, dataset discovery, "
                "findings, opportunities, and submission planning."
            ),
            heading("Operating Model"),
            bullet(
                "GitHub is the source of truth for canonical markdown, scripts, prompts, and outputs."
            ),
            bullet("Notion is the collaboration and planning layer."),
            bullet("ChatGPT Group Chat is the discussion and brainstorming layer."),
        ],
    )

    print("Creating Repo Pages database...")

    repo_pages_db_id = client.create_database(
        parent_page_id=hub_id,
        title="Repo Pages",
        properties={
            "Name": title_property(),
            "Repo Path": text_property(),
            "Category": select_property(
                ["wiki", "research", "findings", "prompts", "readme"]
            ),
            "Last Synced": date_property(),
            "GitHub URL": url_property(),
            "Content Hash": text_property(),
            "Status": select_property(["Active", "Archived", "Draft"]),
        },
    )

    print("Creating Dataset Inventory database...")

    dataset_inventory_db_id = client.create_database(
        parent_page_id=hub_id,
        title="Dataset Inventory",
        properties={
            "Dataset": title_property(),
            "Source": select_property(
                ["data.gov", "CDC", "NIH", "HHS", "PubMed", "Other"]
            ),
            "URL": url_property(),
            "Relevance": select_property(["High", "Medium", "Low", "Unknown"]),
            "Quality": select_property(["High", "Medium", "Low", "Unknown"]),
            "Status": select_property(
                ["Not reviewed", "Reviewed", "Promising", "Rejected"]
            ),
            "Notes": text_property(),
        },
    )

    print("Creating Research Questions database...")

    research_questions_db_id = client.create_database(
        parent_page_id=hub_id,
        title="Research Questions",
        properties={
            "Question": title_property(),
            "Category": select_property(
                ["data", "users", "disease", "workflow", "AI", "submission"]
            ),
            "Priority": select_property(["High", "Medium", "Low"]),
            "Status": select_property(["Open", "In progress", "Answered", "Parked"]),
            "Answer Summary": text_property(),
        },
    )

    print("Creating Findings Log database...")

    findings_log_db_id = client.create_database(
        parent_page_id=hub_id,
        title="Findings Log",
        properties={
            "Finding": title_property(),
            "Evidence URL": url_property(),
            "Confidence": select_property(["High", "Medium", "Low"]),
            "Category": select_property(
                ["dataset", "user pain", "AI opportunity", "submission", "risk"]
            ),
            "Date Found": date_property(),
            "Action Needed": checkbox_property(),
            "Notes": text_property(),
        },
    )

    print("Creating Opportunities database...")

    opportunities_db_id = client.create_database(
        parent_page_id=hub_id,
        title="Opportunities",
        properties={
            "Opportunity": title_property(),
            "User": text_property(),
            "Problem": text_property(),
            "AI Angle": text_property(),
            "Feasibility": number_property(),
            "Impact": number_property(),
            "Priority": select_property(["High", "Medium", "Low"]),
            "Status": select_property(
                ["Idea", "Investigating", "Shortlisted", "Rejected"]
            ),
        },
    )

    print("Creating Submission Plan page...")

    submission_plan_id = client.create_page(
        parent_page_id=hub_id,
        title="Submission Plan",
        children=[
            heading("Phase 1 Deliverables"),
            todo("Confirm exact submission requirements."),
            todo("Identify strongest public datasets."),
            todo("Select core problem/opportunity."),
            todo("Draft solution concept."),
            todo("Review scoring rubric."),
            heading("Submission Narrative"),
            bullet("Problem"),
            bullet("Users"),
            bullet("Data sources"),
            bullet("Proposed AI solution"),
            bullet("Evidence"),
            bullet("Risks"),
            bullet("Implementation path"),
        ],
    )

    print("\nDone.")
    print(f"Hub page ID: {hub_id}")
    print(f"Repo Pages DB ID: {repo_pages_db_id}")
    print(f"Dataset Inventory DB ID: {dataset_inventory_db_id}")
    print(f"Research Questions DB ID: {research_questions_db_id}")
    print(f"Findings Log DB ID: {findings_log_db_id}")
    print(f"Opportunities DB ID: {opportunities_db_id}")
    print(f"Submission Plan page ID: {submission_plan_id}")

    print("\nSave the Repo Pages DB ID. We'll need it for GitHub -> Notion sync.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
