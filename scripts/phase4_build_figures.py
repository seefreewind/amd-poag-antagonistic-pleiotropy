#!/usr/bin/env python3
"""Build Phase 4 manuscript figures from frozen Phase 4 TSV/JSON outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "results/figures"
FIG.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
})

BLUE = "#2f6f8f"
ORANGE = "#c8873e"
GRAY = "#6f7782"
GREEN = "#4f8662"
RED = "#b24c4c"
LIGHT = "#eef2f4"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def f(value: str) -> float:
    return float(value)


def save_pub(fig: mpl.figure.Figure, stem: Path) -> None:
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig4() -> None:
    lava = {r["locus"]: r for r in read_tsv(ROOT / "results/phase4/lava/LAVA_BIVARIATE.tsv")}
    global_rg = {"label": "Global LDSC", "estimate": -0.1798, "lo": -0.1798 - 1.96 * 0.0665, "hi": -0.1798 + 1.96 * 0.0665, "color": GRAY}
    local = [
        {"label": "L006 LAVA", "estimate": f(lava["L006"]["rho"]), "lo": f(lava["L006"]["rho.lower"]), "hi": f(lava["L006"]["rho.upper"]), "color": BLUE},
        {"label": "L007 LAVA", "estimate": f(lava["L007"]["rho"]), "lo": f(lava["L007"]["rho.lower"]), "hi": f(lava["L007"]["rho.upper"]), "color": ORANGE},
    ]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={"width_ratios": [1, 1.15]})
    ax = axes[0]
    items = [global_rg] + local
    ys = np.arange(len(items))[::-1]
    for y, item in zip(ys, items):
        ax.errorbar(item["estimate"], y, xerr=[[item["estimate"] - item["lo"]], [item["hi"] - item["estimate"]]],
                    fmt="o", color=item["color"], ecolor=item["color"], elinewidth=1.6, capsize=3, markersize=5)
    ax.axvline(0, color="#222222", lw=0.8, ls="--")
    ax.set_yticks(ys, [x["label"] for x in items])
    ax.set_xlim(-1, 0.8)
    ax.set_xlabel("Local or global genetic correlation")
    ax.set_title("Global signal and two-locus sensitivity", loc="left", fontsize=9, weight="bold")
    ax.grid(axis="x", color="#d8dde0", lw=0.5)
    ax.set_axisbelow(True)

    ax = axes[1]
    comp = read_tsv(ROOT / "results/phase4/LAVA_HDLL_COMPARISON.tsv")
    items2 = [
        ("L006 LAVA", f(lava["L006"]["rho"]), f(lava["L006"]["rho.lower"]), f(lava["L006"]["rho.upper"]), BLUE),
        ("L006 HDL-L chr22.12", f(comp[0]["hdl_rg"]), f(comp[0]["hdl_lower"]), f(comp[0]["hdl_upper"]), "#5f8ea7"),
        ("L007 LAVA", f(lava["L007"]["rho"]), f(lava["L007"]["rho.lower"]), f(lava["L007"]["rho.upper"]), ORANGE),
        ("L007 HDL-L chr22.16", f(comp[3]["hdl_rg"]), f(comp[3]["hdl_lower"]), f(comp[3]["hdl_upper"]), "#d5a66b"),
    ]
    ys = np.arange(len(items2))[::-1]
    for y, (label, est, lo, hi, color) in zip(ys, items2):
        ax.errorbar(est, y, xerr=[[est - lo], [hi - est]], fmt="o", color=color, ecolor=color, elinewidth=1.4, capsize=3, markersize=5)
    ax.axvline(0, color="#222222", lw=0.8, ls="--")
    ax.set_yticks(ys, [x[0] for x in items2])
    ax.set_xlim(-1, 1)
    ax.set_xlabel("Local genetic correlation")
    ax.set_title("LAVA versus overlapping HDL-L blocks", loc="left", fontsize=9, weight="bold")
    ax.grid(axis="x", color="#d8dde0", lw=0.5)
    ax.set_axisbelow(True)
    fig.suptitle("Phase 4 local architecture sensitivity", fontsize=10, weight="bold", x=0.03, ha="left")
    fig.text(0.03, 0.02, "Intervals: 95% CI; global interval uses LDSC SE", fontsize=7, color=GRAY)
    fig.text(0.52, 0.02, "HDL-L bounds may be clipped at ±1; no local estimate passed BH-FDR", fontsize=7, color=GRAY)
    fig.tight_layout(rect=[0, 0.08, 1, 0.93])
    save_pub(fig, FIG / "Figure4_phase4_local_rg_comparison")


def fig5() -> None:
    rows = [
        ("Shared discovery", "3/3 target variants", "3/3 target variants"),
        ("Quantitative EUR LD", "737/738; PSD PASS", "720/723; PSD PASS"),
        ("Unified SuSiE", "1 AMD + 3 POAG signals", "3 AMD + 1 POAG signal"),
        ("Unified coloc PP4", "0.9756", "0.9678"),
        ("Signal-level CS overlap", "n = 10", "n = 3"),
        ("Harmonized direction", "OPPOSITE", "CONCORDANT"),
        ("LAVA local estimate", "rho = −0.332; P = 0.0942", "rho = 0.067; P = 0.6396"),
        ("Final evidence category", "Candidate opposite-effect\nshared signal", "Concordant shared-signal\ncontrast"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.45), gridspec_kw={"wspace": 0.06})
    for col, (ax, title, accent) in enumerate(zip(axes, ["L006", "L007"], [BLUE, ORANGE])):
        ax.set_xlim(0, 1); ax.set_ylim(-0.9, len(rows) + 0.55); ax.axis("off")
        ax.add_patch(plt.Rectangle((0.0, len(rows) - 0.05), 1.0, 0.58, color=accent, alpha=0.13, lw=0))
        ax.text(0.04, len(rows) + 0.24, title, fontsize=11, weight="bold", color=accent, va="center")
        ax.text(0.04, len(rows) - 0.34, "Evidence item", fontsize=7.4, weight="bold", color=GRAY)
        ax.text(0.52, len(rows) - 0.34, "Frozen result", fontsize=7.4, weight="bold", color=GRAY)
        for i, (label, l006_note, l007_note) in enumerate(rows):
            y = len(rows) - 0.95 - i
            note = l006_note if col == 0 else l007_note
            ax.plot([0.03, 0.97], [y - 0.28, y - 0.28], color="#e0e5e8", lw=0.6)
            ax.text(0.04, y, label, va="center", fontsize=7.25)
            ax.text(0.52, y, note, va="center", fontsize=7.25, color=GRAY)
    fig.suptitle("Paired direction-resolved evidence adjudication", fontsize=10, weight="bold", x=0.03, ha="left")
    fig.text(0.03, 0.015, "Shared-signal support and direction are reported separately; PP4 and credible-set overlap do not establish a shared causal variant", fontsize=7, color=GRAY)
    fig.tight_layout(rect=[0, 0.055, 1, 0.94])
    save_pub(fig, FIG / "Figure5_L006_L007_direction_resolved_adjudication")


def fig6() -> None:
    rows = read_tsv(ROOT / "results/phase4/FINAL_ANTAGONISTIC_TIER_TABLE_PHASE4.tsv")
    categories = {
        "Candidate opposite-effect\nshared signal": sum(r["phase4_final_tier"] == "TIER1" for r in rows),
        "Opposite-direction\nshared discovery": sum(r["phase4_final_tier"] == "TIER3" for r in rows),
        "Concordant shared\nsignal": sum(r["phase4_final_tier"] == "CONCORDANT" for r in rows),
    }
    colors = [BLUE, "#b7c3c9", ORANGE]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={"width_ratios": [1.0, 1.3]})
    ax = axes[0]
    labels = list(categories)
    vals = list(categories.values())
    bars = ax.bar(np.arange(len(labels)), vals, color=colors, width=0.68)
    ax.set_ylim(0, max(vals) + 1.5); ax.set_ylabel("Number of loci")
    ax.set_title("Final evidence categories", loc="left", fontsize=9, weight="bold")
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=25, ha="right", rotation_mode="anchor")
    for b, v in zip(bars, vals): ax.text(b.get_x() + b.get_width()/2, v + 0.1, str(v), ha="center", fontsize=8, weight="bold")
    ax.grid(axis="y", color="#d8dde0", lw=0.5); ax.set_axisbelow(True)

    ax = axes[1]
    summary = [("Global LDSC", -0.1798, GRAY), ("L006", -0.3320, BLUE), ("L007", 0.0672, ORANGE)]
    ys = np.arange(len(summary))[::-1]
    for y, (label, value, color) in zip(ys, summary):
        ax.barh(y, value, color=color, alpha=0.88, height=0.48)
        ax.text(value - 0.015 if value < 0 else value + 0.015, y, f"{value:.3f}", va="center", ha="right" if value < 0 else "left", fontsize=8)
    ax.axvline(0, color="#222222", lw=0.8)
    ax.set_yticks(ys, [x[0] for x in summary]); ax.set_xlim(-0.45, 0.2)
    ax.set_xlabel("Genetic correlation estimate")
    ax.set_title("Direction-resolved summary", loc="left", fontsize=9, weight="bold")
    ax.grid(axis="x", color="#d8dde0", lw=0.5); ax.set_axisbelow(True)
    fig.suptitle("Direction-resolved architecture summary", fontsize=10, weight="bold", x=0.03, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    save_pub(fig, FIG / "Figure6_phase4_architecture_summary")


def main() -> None:
    fig4(); fig5(); fig6()
    print("phase4_figures_complete")


if __name__ == "__main__":
    main()
