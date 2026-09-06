# Final-Year-Project— Stage 1

VeriModern is a verification-first project for behavior-preserving legacy Java modernization.

Stage 1 creates a baseline report for a legacy Maven project before any transformation is attempted. The report is the evidence used by later AI-assisted modernization stages.

## What Stage 1 does

1. Validates a selected Maven project.
2. Detects the active Java version.
3. Runs `mvn test` without modifying the project.
4. Writes a timestamped JSON baseline report.

## Prerequisites

- Python 3.9+
- Maven on `PATH`
- A JDK able to build the chosen Maven project

## Run the bundled example

```bash
python3 main.py baseline --project-path fixtures/legacy-banking-app
```

Reports are written to `reports/` by default. To choose another location:

```bash
python3 main.py baseline \
  --project-path fixtures/legacy-banking-app \
  --reports-dir /absolute/path/to/reports
```

## Run Python tests

```bash
python3 -m unittest discover -s tests -v
```

## Stage 1 boundary

This stage does **not** transform source code, call an LLM, provide a web UI, or use a database. It only captures the original test outcome safely and reproducibly.
