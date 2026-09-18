import argparse
import json
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parent.parent / "data" / "relationships.json").read_text(encoding="utf-8"))

def main():
    p = argparse.ArgumentParser(description="Query NVIDIA relationship research data")
    p.add_argument("--type", choices=["supplier","customer","partner","investor","peer"])
    p.add_argument("--target")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    rows = DATA
    if args.type:
        rows = [r for r in rows if r["relationship"] == args.type]
    if args.target:
        rows = [r for r in rows if r["target"].lower() == args.target.lower()]

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for r in rows:
            print(f'{r["source"]} --{r["relationship"]}--> {r["target"]} [{r["status"]}]')

if __name__ == "__main__":
    main()
