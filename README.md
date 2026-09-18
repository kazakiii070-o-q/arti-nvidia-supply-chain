# NVIDIA Supply Chain & Corporate Relationship Research

A reproducible research dataset and small HTTP/CLI service mapping publicly documented relationships around NVIDIA Corporation.

**Research cutoff:** 2026-09-18

## What this project does

The project converts public corporate disclosures into structured relationship records:

- supplier
- customer / documented deployment relationship
- partner
- investor
- peer / competitor

Each relationship keeps its evidence trail instead of presenting an unsupported conclusion.

## Why the evidence model is conservative

NVIDIA's SEC filings distinguish direct customers from indirect customers. The current filing says direct customers include AIBs, distributors, ODMs, OEMs, CSPs, AI model makers and system integrators, while indirect customers can include CSPs, AI clouds, AI model makers, enterprises and public-sector entities. Therefore, a company mentioned in a deployment announcement is not automatically labeled a direct customer.

## Repository structure

```text
data/relationships.json       # main research dataset
fixtures/                     # deterministic test data
src/api.py                    # HTTP JSON API
src/cli.py                    # command-line interface
scripts/validate_data.py      # schema and URL validation
tests/                        # automated tests
docs/evidence-policy.md      # evidence rules
```

## Quick start

```bash
python -m venv .venv
# activate the virtual environment
pip install -r requirements.txt

python scripts/validate_data.py
pytest

uvicorn src.api:app --reload
```

API examples:

```text
GET /health
GET /summary
GET /companies/NVIDIA/relationships
GET /companies/NVIDIA/relationships?type=supplier
GET /relationships/Marvell%20Technology
```

CLI examples:

```bash
python -m src.cli --type supplier
python -m src.cli --target "Marvell Technology"
python -m src.cli --type investor --json
```

## Evidence rules

Relationship records should contain:

- publisher
- publication date
- source URL
- evidence locator
- research cutoff
- relationship status

Primary sources are preferred, especially SEC filings and NVIDIA/counterparty disclosures.

## Scope and limitations

This is a corporate-relationship research dataset, not an investment recommendation or price forecast.

A relationship may change after the research cutoff. Historical evidence is retained with its original publication date rather than being presented as a current fact.

## Current dataset

The project currently contains 35 relationship records across the five requested relationship categories. The dataset is intentionally smaller than a broad web crawl because each record is expected to have an identifiable evidence trail.
