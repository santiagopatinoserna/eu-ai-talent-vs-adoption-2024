"""
Build three charts for the post:

  chart_scatter_talent_vs_ai.png  ── Main scatter: ICT supply vs AI adoption
  chart_graduates_per_100k.png    ── Spain in top 5 for ICT graduates per capita
  chart_utilization_gap.png       ── AI per ICT specialist ratio (utilization)

Run from repo root:  python scripts/chart.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
CHARTS_DIR = os.path.join(REPO_ROOT, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(DATA_DIR, "talent_vs_adoption.csv"))

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "-",
    "grid.linewidth": 0.5,
})
ACCENT = "#0B5FFF"
HIGHLIGHT = "#E33E2B"
ORANGE = "#F4A23E"
GREEN = "#1F9D55"
MUTED = "#9AA3AE"
INK = "#0E1116"
BG = "#FFFFFF"


def add_titles(fig, title, subtitle):
    fig.text(0.06, 0.965, title, fontsize=18, fontweight="bold", color=INK, ha="left", va="top")
    fig.text(0.06, 0.918, subtitle, fontsize=12, color="#333", ha="left", va="top")


def add_footer(fig, source, credit="Chart by Santiago Patiño Serna"):
    fig.text(0.06, 0.015, source, fontsize=8.5, color="#666", ha="left", va="bottom", linespacing=1.5)
    fig.text(0.98, 0.015, credit, fontsize=8.5, color="#666", ha="right", va="bottom")


# CHART 1 — SCATTER
fig, ax = plt.subplots(figsize=(12, 9.5), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.97, top=0.84, bottom=0.12)

UNDER = {"Spain", "France", "Italy", "Poland", "Romania", "Hungary", "Bulgaria", "Estonia", "Ireland", "Lithuania", "Portugal"}
OVER = {"Slovenia", "Denmark", "Belgium", "Greece", "Germany", "Austria"}

x = df["ict_pct_employment"].values
y = df["ai_adoption_pct_2024"].values
slope, intercept = np.polyfit(x, y, 1)
xfit = np.linspace(x.min() - 0.3, x.max() + 0.3, 50)
ax.plot(xfit, slope * xfit + intercept, "--", color="#888", linewidth=1.5, alpha=0.7, label="Average relationship (r=0.72)")

for _, row in df.iterrows():
    c = "#6B7280"; s = 90
    if row["geo_label"] == "Spain":
        c = HIGHLIGHT; s = 220
    elif row["geo_label"] == "France":
        c = ORANGE; s = 220
    elif row["geo_label"] in OVER:
        c = GREEN; s = 110
    elif row["geo_label"] in UNDER:
        c = "#C0392B"; s = 90
    ax.scatter(row["ict_pct_employment"], row["ai_adoption_pct_2024"],
               s=s, color=c, alpha=0.85, edgecolor="white", linewidth=1.2, zorder=3)

LABEL = {
    "Spain": ("Spain", "right", -14, 0, HIGHLIGHT, "bold"),
    "France": ("France", "right", -14, 0, ORANGE, "bold"),
    "Germany": ("Germany", "left", 10, 0, GREEN, "bold"),
    "Slovenia": ("Slovenia", "left", 10, -4, GREEN, "bold"),
    "Denmark": ("Denmark", "left", 10, 5, GREEN, "bold"),
    "Belgium": ("Belgium", "left", 10, -10, GREEN, "bold"),
    "Sweden": ("Sweden", "left", 10, 0, INK, "normal"),
    "Finland": ("Finland", "left", 10, 5, INK, "normal"),
    "Netherlands": ("Netherlands", "left", 10, -5, INK, "normal"),
    "Estonia": ("Estonia", "left", 10, 0, "#C0392B", "normal"),
    "Ireland": ("Ireland", "left", 10, 0, "#C0392B", "normal"),
    "Italy": ("Italy", "left", 10, -10, "#C0392B", "normal"),
    "Romania": ("Romania", "left", 10, 0, "#C0392B", "normal"),
    "Poland": ("Poland", "left", 10, 4, "#C0392B", "normal"),
    "Greece": ("Greece", "right", -12, -4, GREEN, "normal"),
}
for _, row in df.iterrows():
    n = row["geo_label"]
    if n not in LABEL: continue
    txt, ha, dx, dy, color, weight = LABEL[n]
    ax.annotate(txt, xy=(row["ict_pct_employment"], row["ai_adoption_pct_2024"]),
                xytext=(dx, dy), textcoords="offset points",
                fontsize=10, color=color, fontweight=weight, ha=ha, va="center")

ax.axvline(df["ict_pct_employment"].median(), color="#DDD", linewidth=0.7, zorder=0)
ax.axhline(df["ai_adoption_pct_2024"].median(), color="#DDD", linewidth=0.7, zorder=0)
ax.text(0.98, 0.02, "LOW talent  •  LOW AI", transform=ax.transAxes, fontsize=9, color="#999", ha="right", va="bottom", style="italic")
ax.text(0.02, 0.02, "Wasted talent  ↓", transform=ax.transAxes, fontsize=9, color="#999", ha="left", va="bottom", style="italic")
ax.text(0.98, 0.98, "HIGH talent  •  HIGH AI", transform=ax.transAxes, fontsize=9, color="#999", ha="right", va="top", style="italic")
ax.text(0.02, 0.98, "Punching above weight  ↑", transform=ax.transAxes, fontsize=9, color="#999", ha="left", va="top", style="italic")

ax.set_xlabel("ICT specialists as % of total employment, 2024  (talent supply)", fontsize=11, color="#444", labelpad=10)
ax.set_ylabel("% of enterprises (10+ employees) using AI, 2024  (deployment)", fontsize=11, color="#444", labelpad=10)
ax.set_xlim(1.0, 9.5); ax.set_ylim(0, 32)
ax.legend(loc="lower right", frameon=False, fontsize=10)

add_titles(fig,
           "Same talent supply, very different AI adoption",
           "Each dot = a European country. X = ICT specialist supply. Y = enterprise AI adoption. Spain & France fall way below the average line.")
add_footer(fig,
           "Sources: Eurostat isoc_sks_itspt (ICT specialists, 2024) + educ_uoe_grad02 (ICT graduates 2023) + isoc_eb_ai (AI adoption, 2024).\n"
           "31 countries with full data. Correlation Pearson 0.722, Spearman 0.776 (n=31).")
plt.savefig(os.path.join(CHARTS_DIR, "chart_scatter_talent_vs_ai.png"), dpi=200, facecolor=BG)
print("Saved charts/chart_scatter_talent_vs_ai.png"); plt.close()


# CHART 2 — graduates per 100k
df_g = df.dropna(subset=["ict_graduates_per_100k"]).sort_values("ict_graduates_per_100k", ascending=True).copy()
fig, ax = plt.subplots(figsize=(11, 11), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.22, right=0.95, top=0.86, bottom=0.10)

colors2 = [HIGHLIGHT if n == "Spain" else (ORANGE if n == "France" else MUTED) for n in df_g["geo_label"]]
bars = ax.barh(df_g["geo_label"], df_g["ict_graduates_per_100k"], color=colors2, edgecolor="none", height=0.72)
for bar, v, n in zip(bars, df_g["ict_graduates_per_100k"], df_g["geo_label"]):
    c = HIGHLIGHT if n == "Spain" else (ORANGE if n == "France" else INK)
    w = "bold" if n in ("Spain", "France") else "normal"
    ax.text(v + 1.5, bar.get_y() + bar.get_height()/2, f"{v:.1f}", va="center", ha="left", fontsize=10.5, color=c, fontweight=w)

spain_y = list(df_g["geo_label"]).index("Spain")
ax.annotate("Spain trains MORE ICT grads per capita\nthan Germany, France, EU average.\nSpain ranks 15/32 in AI adoption.",
            xy=(65.7, spain_y), xytext=(95, spain_y - 4),
            fontsize=11, color=HIGHLIGHT, fontweight="bold", ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1.4, connectionstyle="arc3,rad=-0.2"))
france_y = list(df_g["geo_label"]).index("France")
ax.annotate("France: above EU average for\ntalent pipeline. Last in Western\nEurope for enterprise AI use.",
            xy=(48.7, france_y), xytext=(95, france_y + 3),
            fontsize=10.5, color=ORANGE, fontweight="bold", ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2, connectionstyle="arc3,rad=0.2"))

ax.set_xlim(0, 175)
ax.set_xlabel("ICT graduates per 100,000 inhabitants, 2023  (talent pipeline)", fontsize=11, color="#444", labelpad=10)
add_titles(fig,
           "Europe's ICT talent pipeline — Spain is in the top 5",
           "Annual ICT tertiary graduates (ISCED 5–8) per 100,000 inhabitants, by country.")
add_footer(fig,
           "Sources: Eurostat educ_uoe_grad02 (ICT graduates 2023) + demo_pjan (population 2024).\n"
           "Field of education F06 (Information and Communication Technologies), all tertiary levels.")
plt.savefig(os.path.join(CHARTS_DIR, "chart_graduates_per_100k.png"), dpi=200, facecolor=BG)
print("Saved charts/chart_graduates_per_100k.png"); plt.close()


# CHART 3 — utilization ratio
df_u = df.sort_values("ai_per_ict_ratio", ascending=True).copy()
fig, ax = plt.subplots(figsize=(11, 10.5), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.22, right=0.95, top=0.84, bottom=0.10)

med = df_u["ai_per_ict_ratio"].median()
colors3 = []
for n, r in zip(df_u["geo_label"], df_u["ai_per_ict_ratio"]):
    if n == "Spain": colors3.append(HIGHLIGHT)
    elif n == "France": colors3.append(ORANGE)
    elif r < med * 0.75: colors3.append("#C0392B")
    elif r > med * 1.4: colors3.append(GREEN)
    else: colors3.append(MUTED)

bars = ax.barh(df_u["geo_label"], df_u["ai_per_ict_ratio"], color=colors3, edgecolor="none", height=0.72)
for bar, v, n in zip(bars, df_u["ai_per_ict_ratio"], df_u["geo_label"]):
    c = HIGHLIGHT if n == "Spain" else (ORANGE if n == "France" else INK)
    w = "bold" if n in ("Spain", "France") else "normal"
    ax.text(v + 0.07, bar.get_y() + bar.get_height()/2, f"{v:.2f}", va="center", ha="left", fontsize=10.5, color=c, fontweight=w)

eu_median = df_u["ai_per_ict_ratio"].median()
ax.axvline(eu_median, color="#888", linestyle="--", linewidth=1, alpha=0.7)
ax.text(eu_median + 0.05, len(df_u) - 1, f"Median: {eu_median:.2f}", fontsize=9, color="#666", va="center", style="italic")

ax.set_xlim(0, 5.5)
ax.set_xlabel("AI adoption % ÷ ICT specialists %  (how much AI use per unit of talent)", fontsize=11, color="#444", labelpad=10)
add_titles(fig,
           "Talent utilization ratio — same talent, very different outcomes",
           "Higher = more AI adoption per unit of ICT talent supply. Lower = talent on the table.")
add_footer(fig,
           "Sources: Eurostat isoc_sks_itspt + isoc_eb_ai (2024). Ratio = % enterprises using AI ÷ % workforce in ICT.\n"
           "Excludes EU/EA aggregates. 31 countries.")
plt.savefig(os.path.join(CHARTS_DIR, "chart_utilization_gap.png"), dpi=200, facecolor=BG)
print("Saved charts/chart_utilization_gap.png"); plt.close()
