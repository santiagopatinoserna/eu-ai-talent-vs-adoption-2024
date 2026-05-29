"""
Cross-reference:
  - ICT specialist supply (% of total employment, Eurostat 2024)
  - ICT graduates per 100k inhabitants (Eurostat 2023)
  - AI adoption % from companion repo (Eurostat 2024, bundled in data/)

Output: data/talent_vs_adoption.csv

Run from repo root:  python scripts/analyze.py
"""
import json, os, itertools
import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")


def jsonstat_to_long(path):
    raw = json.load(open(path))
    dim_ids = raw["id"]
    sizes = raw["size"]
    dims = {d: raw["dimension"][d] for d in dim_ids}
    def codes(d):
        idx = dims[d]["category"]["index"]
        return sorted(idx.keys(), key=lambda k: idx[k])
    dim_codes = {d: codes(d) for d in dim_ids}
    dim_labels = {d: dims[d]["category"]["label"] for d in dim_ids}
    rows = []
    for combo in itertools.product(*[range(s) for s in sizes]):
        flat = 0
        stride = 1
        for j in reversed(range(len(sizes))):
            flat += combo[j] * stride
            stride *= sizes[j]
        v = raw["value"].get(str(flat))
        if v is None:
            continue
        rows.append({dim_ids[j]: dim_codes[dim_ids[j]][combo[j]] for j in range(len(sizes))} | {"value": v})
    df = pd.DataFrame(rows)
    if "geo" in df.columns:
        df["geo_label"] = df["geo"].map(dim_labels["geo"])
    return df


ict = jsonstat_to_long(os.path.join(DATA_DIR, "ict_specialists_raw.json"))
ict_pct = ict[ict["unit"] == "PC_EMP"][["geo", "geo_label", "value"]].rename(columns={"value": "ict_pct_employment"})
ict_n = ict[ict["unit"] == "THS_PER"][["geo", "value"]].rename(columns={"value": "ict_specialists_thousands"})
ict_full = ict_pct.merge(ict_n, on="geo")

grad = jsonstat_to_long(os.path.join(DATA_DIR, "ict_graduates_raw.json"))
grad_clean = grad[["geo", "geo_label", "value"]].rename(columns={"value": "ict_graduates_2023"})

pop = jsonstat_to_long(os.path.join(DATA_DIR, "population_raw.json"))
pop_clean = pop[["geo", "value"]].rename(columns={"value": "population_2024"})

df = ict_full.merge(grad_clean, on=["geo", "geo_label"], how="left").merge(pop_clean, on="geo", how="left")
df["ict_graduates_per_100k"] = (df["ict_graduates_2023"] / df["population_2024"] * 100_000).round(1)

ai = pd.read_csv(os.path.join(DATA_DIR, "ai_tany_all.csv"))
ai_ge10 = ai[ai["size_emp"] == "GE10"][["geo", "value"]].rename(columns={"value": "ai_adoption_pct_2024"})
df = df.merge(ai_ge10, on="geo", how="left")
df = df[~df["geo"].str.startswith(("EU", "EA"))].copy()
df = df.dropna(subset=["ict_pct_employment", "ai_adoption_pct_2024"]).reset_index(drop=True)
df["ai_per_ict_ratio"] = (df["ai_adoption_pct_2024"] / df["ict_pct_employment"]).round(2)

corr_p = df[["ict_pct_employment", "ai_adoption_pct_2024"]].corr().iloc[0, 1]
corr_s = df[["ict_pct_employment", "ai_adoption_pct_2024"]].corr(method="spearman").iloc[0, 1]
print(f"=== Correlation (n={len(df)}) ===")
print(f"  Pearson:  {corr_p:.3f}")
print(f"  Spearman: {corr_s:.3f}")

print("\n=== UNDER-USING TALENT (low AI/ICT ratio) ===")
print(df.sort_values("ai_per_ict_ratio").head(10)[
    ["geo_label", "ict_pct_employment", "ict_graduates_per_100k", "ai_adoption_pct_2024", "ai_per_ict_ratio"]
].to_string(index=False))

print("\n=== PUNCHING ABOVE WEIGHT (high AI/ICT ratio) ===")
print(df.sort_values("ai_per_ict_ratio", ascending=False).head(10)[
    ["geo_label", "ict_pct_employment", "ict_graduates_per_100k", "ai_adoption_pct_2024", "ai_per_ict_ratio"]
].to_string(index=False))

df.to_csv(os.path.join(DATA_DIR, "talent_vs_adoption.csv"), index=False)
print(f"\nSaved data/talent_vs_adoption.csv ({len(df)} countries)")
