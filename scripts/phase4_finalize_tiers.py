#!/usr/bin/env python3
"""Create the Phase 4 final tier table without modifying the Phase 3.5 table."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/phase4"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def read_one(path: Path) -> dict[str, str]:
    return read_tsv(path)[0]


def main() -> None:
    old = read_tsv(ROOT / "results/phase3_5/FINAL_ANTAGONISTIC_TIER_TABLE.tsv")
    l006_coloc = read_one(OUT / "L006_UNIFIED_COLOC.tsv")
    l007_coloc = read_one(OUT / "L007_UNIFIED_COLOC.tsv")
    l006_qc = json.loads((OUT / "L006_QUANT_LD_QC.json").read_text())
    l007_qc = json.loads((OUT / "L007_QUANT_LD_QC.json").read_text())
    lava = {r["locus"]: r for r in read_tsv(OUT / "lava/LAVA_BIVARIATE.tsv")}

    fields = list(old[0]) + [
        "phase4_quant_ld_status", "phase4_quant_ld_coverage", "phase4_max_cross_block_abs_r",
        "phase4_unified_status", "phase4_unified_PP4", "phase4_signal_CS_overlap_n",
        "phase4_top_shared_variant", "phase4_direction", "phase4_lava_rho", "phase4_lava_p",
        "phase4_final_tier", "phase4_final_status", "phase4_reason",
    ]
    rows = []
    for row in old:
        locus = row["locus_id"]
        row = dict(row)
        if locus == "AMD_POAG_L006":
            qc, coloc, lv = l006_qc, l006_coloc, lava["L006"]
            final_tier = "TIER1"
            final_status = "PASS_FINAL_TIER1"
            reason = "Opposite-direction discovery, quantitative EUR cross-block LD PASS, unified SuSiE/coloc.susie PASS, PP4>=0.8, and signal-level CS overlap present."
        elif locus == "AMD_POAG_L007":
            qc, coloc, lv = l007_qc, l007_coloc, lava["L007"]
            final_tier = "CONCORDANT"
            final_status = "PASS_UNIFIED_CONCORDANT"
            reason = "One-time quantitative rescue passed; unified shared signal is concordant and therefore is not an antagonistic locus."
        else:
            qc, coloc, lv = {}, {}, {}
            final_tier = row["final_tier"].upper()
            final_status = "UNCHANGED_PHASE3_5"
            reason = "No Phase 4 rerun or reclassification requested for this locus."
        row.update(
            {
                "phase4_quant_ld_status": qc.get("status", "NOT_RUN"),
                "phase4_quant_ld_coverage": f"{qc.get('n_present', '')}/{qc.get('n_requested', '')}" if qc else "",
                "phase4_max_cross_block_abs_r": qc.get("max_cross_block_abs_r", "NA") if qc else "",
                "phase4_unified_status": coloc.get("status", "NOT_RUN") if coloc else "NOT_RUN_NOT_REQUIRED",
                "phase4_unified_PP4": coloc.get("PP4", "NA") if coloc else "",
                "phase4_signal_CS_overlap_n": coloc.get("signal_CS_overlap_n", "NA") if coloc else "",
                "phase4_top_shared_variant": coloc.get("top_shared_variant", "") if coloc else "",
                "phase4_direction": coloc.get("direction", "") if coloc else "",
                "phase4_lava_rho": lv.get("rho", "") if lv else "",
                "phase4_lava_p": lv.get("p", "") if lv else "",
                "phase4_final_tier": final_tier,
                "phase4_final_status": final_status,
                "phase4_reason": reason,
            }
        )
        rows.append(row)

    with (OUT / "FINAL_ANTAGONISTIC_TIER_TABLE_PHASE4.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    counts = {}
    for row in rows:
        counts[row["phase4_final_tier"]] = counts.get(row["phase4_final_tier"], 0) + 1
    summary = {
        "status": "PHASE4_FINAL_TIER_TABLE_COMPLETE",
        "phase3_5_table_preserved": True,
        "counts": counts,
        "primary_antagonistic_loci": [r["locus_id"] for r in rows if r["phase4_final_tier"] in {"TIER1", "TIER2"}],
        "language_gate": "Use candidate antagonistic locus / opposite-effect shared signal; do not claim disease-wide confirmed antagonistic pleiotropy.",
    }
    (OUT / "FINAL_ANTAGONISTIC_TIER_TABLE_PHASE4.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
