"""Validation for a Maven project before any command is executed."""

from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


class ProjectValidationError(ValueError):
    """Raised when a path is not a runnable Maven project."""


def validate_maven_project(project_path: Path) -> dict[str, str]:
    project_path = project_path.expanduser().resolve()
    if not project_path.is_dir():
        raise ProjectValidationError(f"Project directory does not exist: {project_path}")

    pom_path = project_path / "pom.xml"
    if not pom_path.is_file():
        raise ProjectValidationError(f"pom.xml was not found in: {project_path}")

    if shutil.which("mvn") is None:
        raise ProjectValidationError("Maven command 'mvn' was not found on PATH.")

    try:
        root = ET.parse(pom_path).getroot()
    except ET.ParseError as error:
        raise ProjectValidationError(f"pom.xml is not valid XML: {error}") from error

    namespace = {"m": "http://maven.apache.org/POM/4.0.0"}
    artifact_id = root.findtext("m:artifactId", default="unknown-project", namespaces=namespace)
    return {
        "project_path": str(project_path),
        "project_name": artifact_id,
        "pom_path": str(pom_path),
    }
