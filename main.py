#!/usr/bin/env python3
"""Command-line entry point for the VeriModern Stage 1 baseline harness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.baseline import BaselineHarness
from src.reporter import write_report
from src.validator import ProjectValidationError, validate_maven_project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture a test baseline for a legacy Maven project."
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    baseline = subcommands.add_parser(
        "baseline", help="Run Maven tests and save a JSON baseline report."
    )
    baseline.add_argument(
        "--project-path", required=True, help="Path to the Maven project to inspect."
    )
    baseline.add_argument(
        "--reports-dir", default="reports", help="Directory for generated JSON reports."
    )
    return parser


def run_baseline(project_path: Path, reports_dir: Path) -> int:
    try:
        project = validate_maven_project(project_path)
    except ProjectValidationError as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 2

    result = BaselineHarness().run(project)
    report_path = write_report(result, reports_dir)
    print(f"Baseline report written to: {report_path}")
    print(
        f"Build: {result['build_status']} | Tests: "
        f"{result['tests_passed']} passed, {result['tests_failed']} failed"
    )
    return 0 if result["build_status"] == "passed" else 1


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "baseline":
        return run_baseline(Path(args.project_path), Path(args.reports_dir))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
