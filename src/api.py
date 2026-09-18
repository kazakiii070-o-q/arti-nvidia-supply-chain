from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
import json

app = FastAPI(title="NVIDIA Relationship Research API", version="0.1.0")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "relationships.json"
DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))

@app.get("/summary")
def summary():
    counts = {}
    for row in DATA:
        counts[row["relationship"]] = counts.get(row["relationship"], 0) + 1
    return {"company": "NVIDIA", "cutoff": "2026-09-18", "counts": counts, "total": len(DATA)}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/companies/{company}/relationships")
def relationships(company: str, type: str | None = Query(default=None)):
    rows = [r for r in DATA if r["source"].lower() == company.lower()]
    if type:
        rows = [r for r in rows if r["relationship"].lower() == type.lower()]
    if not rows:
        raise HTTPException(status_code=404, detail="No relationships found")
    return {"company": company, "count": len(rows), "relationships": rows}

@app.get("/relationships/{target}")
def by_target(target: str):
    rows = [r for r in DATA if r["target"].lower() == target.lower()]
    if not rows:
        raise HTTPException(status_code=404, detail="No relationship found")
    return {"target": target, "count": len(rows), "relationships": rows}
