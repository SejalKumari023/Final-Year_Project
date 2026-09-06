import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.validator import ProjectValidationError, validate_maven_project


class ValidateMavenProjectTests(unittest.TestCase):
    def test_rejects_missing_directory(self) -> None:
        with self.assertRaises(ProjectValidationError):
            validate_maven_project(Path("/missing/project"))

    def test_rejects_directory_without_pom(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch("src.validator.shutil.which", return_value="mvn"):
            with self.assertRaises(ProjectValidationError):
                validate_maven_project(Path(directory))

    def test_returns_project_metadata(self) -> None:
        pom = """<project xmlns=\"http://maven.apache.org/POM/4.0.0\"><modelVersion>4.0.0</modelVersion><artifactId>demo</artifactId></project>"""
        with tempfile.TemporaryDirectory() as directory, patch("src.validator.shutil.which", return_value="mvn"):
            Path(directory, "pom.xml").write_text(pom, encoding="utf-8")
            metadata = validate_maven_project(Path(directory))
        self.assertEqual(metadata["project_name"], "demo")


if __name__ == "__main__":
    unittest.main()
