"""
Pull Eurostat datasets for the talent-vs-adoption analysis.

  1. isoc_sks_itspt   — Employed ICT specialists (total), 2024 ref year
  2. educ_uoe_grad02  — ICT graduates 2023, ISCED 5-8, field F06
  3. demo_pjan        — Population on 1 January 2024 (for per-capita normalization)

Yesterday's AI adoption data (ai_tany_all.csv, derived from Eurostat
isoc_eb_ai 2024) is bundled in data/ — see github.com/santiagopatinoserna/eu-ai-adoption-2024

Run from repo root:  python scripts/fetch.py
"""
import json, os, urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

REQS = [
    ("isoc_sks_itspt",
     "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
     "isoc_sks_itspt?format=JSON&lang=EN&time=2024",
     "ict_specialists_raw.json"),
    ("educ_uoe_grad02",
     "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
     "educ_uoe_grad02?format=JSON&lang=EN&time=2023&isced11=ED5-8&iscedf13=F06&sex=T",
     "ict_graduates_raw.json"),
    ("demo_pjan",
     "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
     "demo_pjan?format=JSON&lang=EN&time=2024&sex=T&age=TOTAL",
     "population_raw.json"),
]

for code, url, fname in REQS:
    req = urllib.request.Request(url, headers={
        "User-Agent": "santiago-patino-research/1.0 santiagopatinoserna@gmail.com"
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = json.loads(r.read().decode())
    with open(os.path.join(DATA_DIR, fname), "w") as f:
        json.dump(raw, f, indent=2)
    if "error" in raw:
        print(f"  ERROR for {code}: {raw['error']}")
    else:
        print(f"  {code} -> {fname}  ({len(raw.get('value', {}))} cells, updated {raw.get('updated')})")
