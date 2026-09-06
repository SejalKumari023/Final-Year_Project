"""Safe Maven test execution and basic Surefire result parsing."""

from __future__ import annotations

import re
import subprocess
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


_SUMMARY = re.compile(
    r"Tests run:\s*(?P<run>\d+),\s*Failures:\s*(?P<failures>\d+),\s*Errors:\s*(?P<errors>\d+)",
    re.IGNORECASE,
)


class BaselineHarness:
    """Runs Maven tests without using a shell or changing the target project."""

    def run(self, project: dict[str, str]) -> dict[str, object]:
        started_at = datetime.now(timezone.utc)
        started = time.monotonic()
        completed = subprocess.run(
            ["mvn", "test", "-q"],
            cwd=project["project_path"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
        surefire_results = self._read_surefire_results(Path(project["project_path"]))
        if surefire_results is None:
            tests_run, tests_failed, tests_skipped = self._parse_summary(output)
        else:
            tests_run, tests_failed, tests_skipped = surefire_results
        return {
            "project_name": project["project_name"],
            "project_path": project["project_path"],
            "baseline_created_at": started_at.isoformat(),
            "duration_seconds": round(time.monotonic() - started, 3),
            "command": ["mvn", "test", "-q"],
            "java_version": self._java_version(project["project_path"]),
            "build_status": "passed" if completed.returncode == 0 else "failed",
            "tests_run": tests_run,
            "tests_failed": tests_failed,
            "tests_skipped": tests_skipped,
            "tests_passed": max(tests_run - tests_failed - tests_skipped, 0),
            "exit_code": completed.returncode,
            "output": output[-6000:],
        }

    @staticmethod
    def _parse_summary(output: str) -> tuple[int, int, int]:
        summaries = list(_SUMMARY.finditer(output))
        if not summaries:
            return 0, 0, 0
        tests_run = sum(int(match["run"]) for match in summaries)
        tests_failed = sum(
            int(match["failures"]) + int(match["errors"]) for match in summaries
        )
        return tests_run, tests_failed, 0

    @staticmethod
    def _read_surefire_results(project_path: Path) -> tuple[int, int, int] | None:
        report_files = list((project_path / "target" / "surefire-reports").glob("TEST-*.xml"))
        if not report_files:
            return None

        tests_run = tests_failed = tests_skipped = 0
        for report_file in report_files:
            try:
                suite = ET.parse(report_file).getroot()
            except ET.ParseError:
                continue
            tests_run += int(suite.attrib.get("tests", "0"))
            tests_failed += int(suite.attrib.get("failures", "0")) + int(suite.attrib.get("errors", "0"))
            tests_skipped += int(suite.attrib.get("skipped", "0"))
        return tests_run, tests_failed, tests_skipped

    @staticmethod
    def _java_version(project_path: str) -> str:
        completed = subprocess.run(
            ["mvn", "-q", "help:evaluate", "-Dexpression=maven.compiler.source", "-DforceStdout"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        version = completed.stdout.strip()
        return version if version else "not-declared"
