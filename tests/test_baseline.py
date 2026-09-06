import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.baseline import BaselineHarness


class BaselineHarnessTests(unittest.TestCase):
    @patch("src.baseline.subprocess.run")
    def test_captures_successful_test_summary(self, mock_run) -> None:
        mock_run.side_effect = [
            subprocess.CompletedProcess(["mvn"], 0, "Tests run: 3, Failures: 0, Errors: 0", ""),
            subprocess.CompletedProcess(["mvn"], 0, "1.8\n", ""),
        ]
        result = BaselineHarness().run({"project_name": "demo", "project_path": "/tmp/demo"})
        self.assertEqual(result["build_status"], "passed")
        self.assertEqual(result["tests_run"], 3)
        self.assertEqual(result["tests_passed"], 3)

    @patch("src.baseline.subprocess.run")
    def test_counts_failures_and_errors(self, mock_run) -> None:
        mock_run.side_effect = [
            subprocess.CompletedProcess(["mvn"], 1, "Tests run: 4, Failures: 1, Errors: 1", ""),
            subprocess.CompletedProcess(["mvn"], 0, "1.8\n", ""),
        ]
        result = BaselineHarness().run({"project_name": "demo", "project_path": "/tmp/demo"})
        self.assertEqual(result["build_status"], "failed")
        self.assertEqual(result["tests_failed"], 2)
        self.assertEqual(result["tests_passed"], 2)

    def test_reads_surefire_xml_results(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reports = Path(directory, "target", "surefire-reports")
            reports.mkdir(parents=True)
            Path(reports, "TEST-demo.xml").write_text(
                '<testsuite tests="4" failures="1" errors="1" skipped="1" />', encoding="utf-8"
            )
            self.assertEqual(BaselineHarness._read_surefire_results(Path(directory)), (4, 2, 1))


if __name__ == "__main__":
    unittest.main()
