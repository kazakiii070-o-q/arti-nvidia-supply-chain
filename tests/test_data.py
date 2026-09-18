import json
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parent.parent / "data" / "relationships.json").read_text(encoding="utf-8"))

def test_has_required_fields():
    required = {"source", "relationship", "target", "status", "evidence", "research_cutoff"}
    for row in DATA:
        assert required.issubset(row)
        for field in ["publisher", "published_at", "url", "locator"]:
            assert field in row["evidence"]
        assert row["evidence"]["url"].startswith("http")

def test_required_relationship_types_exist():
    types = {r["relationship"] for r in DATA}
    assert {"supplier", "customer", "partner", "investor", "peer"} <= types

def test_nvidia_is_source():
    assert all(r["source"] == "NVIDIA" for r in DATA)
