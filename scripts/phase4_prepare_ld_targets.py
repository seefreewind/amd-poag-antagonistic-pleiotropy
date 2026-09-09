#!/usr/bin/env python3
"""Prepare frozen-window variant requests, EUR sample IDs, and the Phase 4 LD audit."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE4 = ROOT / "results/phase4"
RAW = ROOT / "data/raw/phase4_ld/1000genomes_phase3"
PANEL = RAW / "integrated_call_samples_v3.20130502.ALL.panel"
VCF = RAW / "ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz"
VCF_TBI = RAW / "ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz.tbi"

AMD = ROOT / "data/processed/phase2_5/ADV_AMD_RESCUE_GRCh37.hm3_noMHC.tsv.gz"
POAG = ROOT / "data/processed/standardized/POAG.hm3_noMHC.tsv.gz"

L006 = (28100711, 30130300)
L007 = (32605227, 33611247)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_region(path: Path, start: int, end: int) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with gzip.open(path, "rt") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if row["CHR"] != "22":
                continue
            bp = int(float(row["BP"]))
            if start <= bp <= end:
                out[row["SNP"]] = row
    return out


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def combine(amd: dict[str, dict[str, str]], poag: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for snp in sorted(set(amd) | set(poag), key=lambda x: (int(amd.get(x, poag.get(x))["BP"]), x)):
        a = amd.get(snp, {})
        p = poag.get(snp, {})
        rows.append(
            {
                "SNP": snp,
                "CHR": int(a.get("CHR", p.get("CHR", 22))),
                "BP": int(float(a.get("BP", p.get("BP", "nan")))),
                "AMD_A1": a.get("A1", ""),
                "AMD_A2": a.get("A2", ""),
                "POAG_A1": p.get("A1", ""),
                "POAG_A2": p.get("A2", ""),
                "AMD_beta": a.get("BETA", ""),
                "AMD_SE": a.get("SE", ""),
                "POAG_beta": p.get("BETA", ""),
                "POAG_SE": p.get("SE", ""),
                "AMD_present": bool(a),
                "POAG_present": bool(p),
            }
        )
    return rows


def main() -> None:
    PHASE4.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    amd_l006 = load_region(AMD, *L006)
    poag_l006 = load_region(POAG, *L006)
    amd_l007 = load_region(AMD, *L007)
    poag_l007 = load_region(POAG, *L007)
    fields = [
        "SNP", "CHR", "BP", "AMD_A1", "AMD_A2", "POAG_A1", "POAG_A2",
        "AMD_beta", "AMD_SE", "POAG_beta", "POAG_SE", "AMD_present", "POAG_present",
    ]
    l006_rows = combine(amd_l006, poag_l006)
    l007_rows = combine(amd_l007, poag_l007)
    write_tsv(PHASE4 / "L006_REQUESTED_VARIANTS.tsv", l006_rows, fields)
    write_tsv(PHASE4 / "L007_REQUESTED_VARIANTS.tsv", l007_rows, fields)
    (PHASE4 / "L006_REQUESTED_IDS.txt").write_text("\n".join(row["SNP"] for row in l006_rows) + "\n")
    (PHASE4 / "L007_REQUESTED_IDS.txt").write_text("\n".join(row["SNP"] for row in l007_rows) + "\n")
    all_ids = sorted({row["SNP"] for row in l006_rows + l007_rows})
    (PHASE4 / "L006_L007_REQUESTED_IDS.txt").write_text("\n".join(all_ids) + "\n")

    candidates = ["rs5749498", "rs756481", "rs12170368"]
    write_tsv(
        PHASE4 / "L007_CANDIDATES.tsv",
        [next(row for row in l007_rows if row["SNP"] == snp) for snp in candidates],
        fields,
    )

    eur_samples: list[str] = []
    with PANEL.open() as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            if row.get("super_pop") == "EUR":
                eur_samples.append(row["sample"])
    (RAW / "EUR.samples.txt").write_text("\n".join(eur_samples) + "\n")

    panel_hash = sha256(PANEL)
    vcf_hash = sha256(VCF)
    tbi_hash = sha256(VCF_TBI)
    source_vcf = "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz"
    source_panel = "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel"
    audit_fields = [
        "reference", "ancestry", "N_ref", "build", "variant_format", "genotype_available",
        "quantitative_LD", "signed_r_available", "L006_coverage", "L007_coverage",
        "download_source", "checksum", "status", "reason",
    ]
    audit = [
        {
            "reference": "HDLL_LD.path_plus_bimfile",
            "ancestry": "UKB_EUR_like",
            "N_ref": "336000_tagged_reference_metadata",
            "build": "GRCh37",
            "variant_format": "LDSVD_with_block_matrices",
            "genotype_available": "FALSE",
            "quantitative_LD": "WITHIN_BLOCK_ONLY",
            "signed_r_available": "WITHIN_BLOCK_ONLY",
            "L006_coverage": "607/607_reference_SNPs_but_no_cross_block_matrix",
            "L007_coverage": "candidate_membership_incomplete",
            "download_source": "local:data/raw/hdll_reference",
            "checksum": "see PHASE3_5 freeze",
            "status": "REJECTED_NOT_CROSS_BLOCK_COMPLETE",
            "reason": "Separate within-block matrices cannot establish cross-block r/r2 or a unified PSD matrix.",
        },
        {
            "reference": "genref_chr22_LDpairs",
            "ancestry": "reference_metadata_not_sufficient_for_quantitative_rescue",
            "N_ref": "not_available",
            "build": "GRCh37",
            "variant_format": "ngCMatrix_binary_adjacency",
            "genotype_available": "FALSE",
            "quantitative_LD": "FALSE",
            "signed_r_available": "FALSE",
            "L006_coverage": "607/607_membership_only",
            "L007_coverage": "3/3_membership_only",
            "download_source": "local:data/raw/phase3_reference/genref",
            "checksum": "see PHASE3_5 freeze",
            "status": "REJECTED_BINARY_ADJACENCY_ONLY",
            "reason": "Binary links cannot be converted into quantitative r2 thresholds.",
        },
        {
            "reference": "LDSC_EUR_weights",
            "ancestry": "EUR",
            "N_ref": "not applicable",
            "build": "GRCh37",
            "variant_format": "LD_scores",
            "genotype_available": "FALSE",
            "quantitative_LD": "FALSE",
            "signed_r_available": "FALSE",
            "L006_coverage": "not applicable",
            "L007_coverage": "not applicable",
            "download_source": "local:data/raw/eur_w_ld_chr",
            "checksum": "see Phase 0/1 manifest",
            "status": "REJECTED_LDSC_SCORES_ONLY",
            "reason": "Per-SNP LD scores are not a pairwise correlation matrix.",
        },
        {
            "reference": "1000G_Phase3_EUR",
            "ancestry": "EUR",
            "N_ref": len(eur_samples),
            "build": "GRCh37",
            "variant_format": "biallelic_SNP_VCF_GT",
            "genotype_available": "TRUE",
            "quantitative_LD": "TRUE",
            "signed_r_available": "TRUE",
            "L006_coverage": "PENDING_target_variant_audit",
            "L007_coverage": "PENDING_candidate_audit",
            "download_source": source_vcf + " ; " + source_panel,
            "checksum": f"VCF:{vcf_hash};TBI:{tbi_hash};PANEL:{panel_hash}",
            "status": "SELECTED_PRIMARY_EUR_LD_PANEL",
            "reason": "Independent public EUR genotype reference with auditable build and quantitative signed dosage correlations.",
        },
    ]
    write_tsv(ROOT / "metadata/PHASE4_LD_REFERENCE_AUDIT.tsv", audit, audit_fields)
    manifest = {
        "primary_reference": "1000G_Phase3_EUR",
        "build": "GRCh37",
        "n_eur_samples": len(eur_samples),
        "eur_sample_file": str(RAW / "EUR.samples.txt"),
        "vcf": str(VCF),
        "vcf_tbi": str(VCF_TBI),
        "vcf_sha256": vcf_hash,
        "vcf_tbi_sha256": tbi_hash,
        "panel_sha256": panel_hash,
        "requested": {
            "L006": {"start": L006[0], "end": L006[1], "n_variants": len(l006_rows)},
            "L007": {"start": L007[0], "end": L007[1], "n_variants": len(l007_rows)},
        },
    }
    (PHASE4 / "PHASE4_LD_RESOURCE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
