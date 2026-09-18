import json
from pathlib import Path

base=Path(__file__).resolve().parent.parent
fixture=json.loads((base/"fixtures"/"sample_relationships.json").read_text(encoding="utf-8"))

def test_fixture_is_deterministic():
    assert len(fixture) == 4
    pairs={(r["relationship"],r["target"]) for r in fixture}
    assert ("supplier","TSMC") in pairs
    assert ("partner","Marvell Technology") in pairs
    assert ("investor","Marvell Technology") in pairs
    assert ("peer","AMD") in pairs
