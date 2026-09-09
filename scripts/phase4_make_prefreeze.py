#!/usr/bin/env python3
"""Create the immutable Phase 4 pre-validation manifest from frozen Phase 3.5 outputs."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main() -> None:
    out = ROOT / "config" / "PHASE4_PREVALIDATION_FREEZE.yaml"
    tier_rows = read_tsv(ROOT / "results/phase3_5/FINAL_ANTAGONISTIC_TIER_TABLE.tsv")
    summary = json.loads((ROOT / "results/phase3_5/PHASE3_PRE_ADJUDICATION_FREEZE_SUMMARY.json").read_text())
    rg_rows = read_tsv(ROOT / "results/phase1/LDSC_RG.tsv")
    rg = next(
        row for row in rg_rows
        if row["trait_a"] == "ADV_AMD"
        and row["trait_b"] == "POAG"
        and row["condition"] == "noMHC"
    )
    l006 = next(row for row in tier_rows if row["locus"] == "AMD_POAG_L006")
    l007 = next(row for row in tier_rows if row["locus"] == "AMD_POAG_L007")

    phase35_cfg = ROOT / "config/PHASE3_5_ANALYSIS_FREEZE.yaml"
    phase35_summary = ROOT / "results/phase3_5/PHASE3_PRE_ADJUDICATION_FREEZE_SUMMARY.json"
    phase35_l006_qc = ROOT / "results/phase3_5/L006_LD_QC.json"
    phase35_l007_qc = ROOT / "results/phase3_5/L007_PROXY_LD_QC.json"

    manifest = {
        "freeze_status": "PHASE4_PREVALIDATION_FROZEN",
        "created": datetime.now().astimezone().isoformat(),
        "scope": {
            "objective": "Quantitative EUR LD rescue for L006/L007 plus orthogonal LAVA local-rg sensitivity",
            "upstream_phase": "PHASE3_5_COMPLETE_MILESTONE_3_PIVOT",
            "new_outputs_root": "results/phase4",
            "new_reports_root": "reports/phase4",
            "no_rerun": [
                "Phase 0-3.5",
                "genome-wide cFDR",
                "genome-wide PLACO",
                "discovery SuSiE/coloc",
                "single-cell/multiome/eQTL/TWAS/MR/drug-target/pathway expansion",
            ],
        },
        "preserve_existing": [
            "config/PHASE0_2_ANALYSIS_FREEZE.yaml",
            "config/PHASE3_ANALYSIS_FREEZE.yaml",
            "config/PHASE3_PRE_ADJUDICATION_FREEZE.yaml",
            "config/PHASE3_5_ANALYSIS_FREEZE.yaml",
            "results/phase0",
            "results/phase1",
            "results/phase2",
            "results/phase2_5",
            "results/phase3",
            "results/phase3_5",
        ],
        "upstream_checksums": {
            "config/PHASE3_5_ANALYSIS_FREEZE.yaml": sha256(phase35_cfg),
            "results/phase3_5/PHASE3_PRE_ADJUDICATION_FREEZE_SUMMARY.json": sha256(phase35_summary),
            "results/phase3_5/L006_LD_QC.json": sha256(phase35_l006_qc),
            "results/phase3_5/L007_PROXY_LD_QC.json": sha256(phase35_l007_qc),
        },
        "global_rg": {
            "trait_a": "Advanced AMD",
            "trait_b": "POAG",
            "condition": "noMHC",
            "rg": float(rg["rg"]),
            "SE": float(rg["rg_se"]),
            "P": float(rg["rg_p"]),
            "BH_FDR": float(rg["fdr_bh"]),
            "major_locus_sensitivity": "negative after APOE, ARMS2/HTRA1, and CFH removal",
            "LOCO": "all 22 chromosome-exclusion estimates remain negative",
            "HDL_L": {
                "tested": "Advanced AMD x POAG",
                "blocks": 2463,
                "finite_rg": 696,
                "minimum_BH_FDR": 0.3007,
                "BH_FDR_below_0_05": 0,
            },
        },
        "phase3_5_discovery": {
            "n_loci": summary["counts"]["n_loci"],
            "n_intersection_variants": summary["counts"]["n_intersection_variants"],
            "n_opposite_direction_loci": summary["counts"]["n_opposite_direction_loci"],
            "tier_counts": {
                "TIER3": sum(row["Tier"] == "TIER3" for row in tier_rows),
                "TIER2": sum(row["Tier"] == "TIER2" for row in tier_rows),
                "TIER1": sum(row["Tier"] == "TIER1" for row in tier_rows),
                "CONCORDANT": sum(row["Tier"] == "CONCORDANT" for row in tier_rows),
                "UNRESOLVED": sum(row["Tier"] == "UNRESOLVED" for row in tier_rows),
            },
        },
        "l006": {
            "frozen_window_GRCh37": "chr22:28600711-29630300",
            "expanded_quantitative_LD_window_GRCh37": "chr22:28100711-30130300",
            "blocks": ["chr22.12", "chr22.13"],
            "block_level_PP4": 0.981761197891504,
            "block_level_CS_overlap_n": 7,
            "phase3_5_cross_block_status": l006["cross_block_QC"],
            "phase3_5_tier": l006["Tier"],
            "direction_audit": "all audited targets opposite",
            "unified_analysis_status": "NOT_RUN_QC_BLOCKED",
        },
        "l007": {
            "frozen_window_GRCh37": "chr22:32605227-33611247",
            "candidates": ["rs5749498", "rs756481", "rs12170368"],
            "phase3_5_quantitative_proxy_status": l007["cross_block_QC"],
            "phase3_5_tier": l007["Tier"],
            "one_time_rescue_rule": "allow unified fine-mapping only if >=2 candidates are directly covered or all have r2>=0.80 proxies",
        },
        "language_gate_before_phase4": {
            "allowed": [
                "negative genetic correlation",
                "opposing genetic architecture",
                "candidate antagonistic region",
                "probable antagonistic locus",
            ],
            "disallowed_until_final_adjudication": [
                "confirmed antagonistic pleiotropy",
                "shared causal variant",
                "causal/protective/therapeutic claims",
            ],
        },
        "phase4_decision_gate": {
            "quantitative_ld_required_for_unified_finemap": True,
            "coloc_PP4_strong": 0.80,
            "coloc_PP4_suggestive_lower": 0.50,
            "proxy_r2_primary": 0.80,
            "proxy_r2_secondary": 0.50,
            "final_freeze_after_validation": True,
        },
    }
    out.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(out)
    print(manifest["upstream_checksums"])


if __name__ == "__main__":
    main()
