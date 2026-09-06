"""Baseline report persistence."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def write_report(result: dict[str, object], reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_project_name = str(result["project_name"]).replace("/", "-")
    report_path = reports_dir / f"baseline-{safe_project_name}-{timestamp}.json"
    report_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return report_path
