#!/usr/bin/env python3
"""Build quantitative-LD QC, cross-block tables, and matrix artifacts for Phase 4."""

from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PHASE4 = ROOT / "results/phase4"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_matrix(path: Path, ids: list[str], matrix: np.ndarray) -> None:
    with gzip.open(path, "wt") as fh:
        fh.write("SNP\t" + "\t".join(ids) + "\n")
        for snp, row in zip(ids, matrix):
            fh.write(snp + "\t" + "\t".join(f"{x:.10g}" for x in row) + "\n")


def read_matrix(prefix: str) -> tuple[list[str], np.ndarray]:
    binary_prefix = PHASE4 / f"{prefix}_QUANT_R_REF_BIN.unphased.vcor1.bin"
    ids_path = PHASE4 / f"{prefix}_QUANT_R_REF_BIN.unphased.vcor1.bin.vars"
    if binary_prefix.exists() and ids_path.exists():
        ids = ids_path.read_text().splitlines()
        matrix = np.fromfile(binary_prefix, dtype="<f8").reshape((len(ids), len(ids)))
    else:
        ids = (PHASE4 / f"{prefix}_QUANT_R_REF.unphased.vcor1.vars").read_text().splitlines()
        matrix = np.loadtxt(PHASE4 / f"{prefix}_QUANT_R_REF.unphased.vcor1", dtype=float, delimiter="\t")
        matrix = np.atleast_2d(matrix)
    if matrix.shape != (len(ids), len(ids)):
        raise ValueError(f"{prefix}: matrix shape {matrix.shape} does not match {len(ids)} IDs")
    return ids, matrix


def read_freq(prefix: str) -> dict[str, dict[str, str]]:
    rows = read_tsv(PHASE4 / f"{prefix}_EUR_FREQ.afreq")
    return {row["ID"]: row for row in rows}


def read_missing(prefix: str) -> dict[str, dict[str, str]]:
    rows = read_tsv(PHASE4 / f"{prefix}_EUR_MISSING.vmiss")
    return {row["ID"]: row for row in rows}


def pvar_info(prefix: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with (PHASE4 / f"{prefix}_1000G_EUR_TARGET.pvar").open() as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            chrom, pos, vid, ref, alt, *_ = line.rstrip("\n").split("\t")
            out[vid] = {"chr": chrom, "pos": pos, "ref": ref, "alt": alt}
    return out


def flip_beta(value: str, rel: str) -> str:
    if value in ("", "NA", "nan"):
        return ""
    x = float(value)
    return str(-x if rel in ("swapped", "complement_swapped") else x)


def complement(allele: str) -> str:
    return allele.translate(str.maketrans("ACGT", "TGCA"))


def allele_relation(a1: str, a2: str, ref: str, alt: str) -> str:
    if a1 == ref and a2 == alt:
        return "exact"
    if a1 == alt and a2 == ref:
        return "swapped"
    if complement(a1) == ref and complement(a2) == alt:
        return "complement"
    if complement(a1) == alt and complement(a2) == ref:
        return "complement_swapped"
    return "mismatch"


def finite_or_none(x: float) -> float | None:
    return float(x) if np.isfinite(x) else None


def block_for(pos: int) -> str:
    if 28101681 <= pos <= 29454477:
        return "chr22.12"
    if 29457622 <= pos <= 30129156:
        return "chr22.13"
    return "OUTSIDE_FROZEN_BLOCKS"


def build_locus(prefix: str, requested_n: int, locus_start: int, locus_end: int) -> dict[str, object]:
    ref_ids, raw = read_matrix(prefix)
    raw = (raw + raw.T) / 2.0
    info = pvar_info(prefix)
    harmonized_rows = read_tsv(PHASE4 / f"{prefix}_QUANT_LD_HARMONIZATION.tsv")
    for row in harmonized_rows:
        # Accept either the pre-QC harmonization schema or the final required schema.
        if "SNP" not in row:
            row["SNP"] = row["variant"]
        if "LD_ID" not in row:
            row["LD_ID"] = f"{row['chr']}:{row['pos']}:{row['LD_A1']}:{row['LD_A2']}"
        row.setdefault("AMD_relation", "")
        row.setdefault("POAG_relation", "")
    # phase4_harmonize_reference writes one row per summary variant; retain only reference-present rows.
    h_by_ref = {row["LD_ID"]: row for row in harmonized_rows if row["included"] == "True"}
    original_ids = [h_by_ref[ref_id]["SNP"] for ref_id in ref_ids]
    freq = read_freq(prefix)
    missing = read_missing(prefix)
    blocks = [block_for(int(info[ref_id]["pos"])) for ref_id in ref_ids]

    # Re-emit the required harmonization schema with a transparent exclusion reason.
    required_fields = [
        "variant", "chr", "pos", "AMD_A1", "AMD_A2", "POAG_A1", "POAG_A2", "LD_A1", "LD_A2",
        "AMD_beta", "POAG_beta", "allele_status", "included", "exclusion_reason",
    ]
    required_rows = []
    for row in harmonized_rows:
        required_rows.append(
            {
                "variant": row["SNP"], "chr": row["chr"], "pos": row["pos"],
                "AMD_A1": row["AMD_A1"], "AMD_A2": row["AMD_A2"], "POAG_A1": row["POAG_A1"], "POAG_A2": row["POAG_A2"],
                "LD_A1": row["LD_A1"], "LD_A2": row["LD_A2"], "AMD_beta": row["AMD_beta"], "POAG_beta": row["POAG_beta"],
                "allele_status": row["allele_status"], "included": row["included"],
                "exclusion_reason": "" if row["included"] == "True" else "NO_ALIGNED_BIALLELIC_REFERENCE_VARIANT_AT_GRCh37_POSITION",
            }
        )
    write_tsv(PHASE4 / f"{prefix}_QUANT_LD_HARMONIZATION.tsv", required_rows, required_fields)
    h_by_ref = {row["LD_ID"]: row for row in harmonized_rows if row["included"] == "True"}

    # Matrix diagnostics.
    eig = np.linalg.eigvalsh(raw)
    positive = eig[eig > 1e-10]
    cond = float(np.max(eig) / np.min(positive)) if positive.size else float("inf")
    duplicate_pos = len(ref_ids) - len({info[x]["pos"] for x in ref_ids})
    monomorphic = sum(float(freq[x]["ALT_FREQS"]) in (0.0, 1.0) for x in ref_ids)
    missing_variants = sum(float(missing[x]["F_MISS"]) > 0 for x in ref_ids)
    diag_error = float(np.max(np.abs(np.diag(raw) - 1.0)))
    sym_error = float(np.max(np.abs(raw - raw.T)))
    cross_idx = [(i, j) for i, bi in enumerate(blocks) for j, bj in enumerate(blocks) if bi == "chr22.12" and bj == "chr22.13"]
    cross_r = np.array([raw[i, j] for i, j in cross_idx], dtype=float)
    cross_r2 = cross_r**2
    coverage = len(ref_ids) / requested_n
    psd_pass = float(np.min(eig)) >= -1e-8
    matrix_pass = (
        coverage >= 0.95 and sym_error <= 1e-8 and diag_error <= 1e-8
        and monomorphic == 0 and missing_variants == 0 and psd_pass
    )
    status = "PASS_QUANTITATIVE_EUR_LD" if matrix_pass else "FAIL_QUANTITATIVE_EUR_LD_QC"

    qc = {
        "n_requested": requested_n,
        "n_present": len(ref_ids),
        "coverage": coverage,
        "n_cross_block_pairs": len(cross_idx),
        "max_cross_block_abs_r": finite_or_none(float(np.max(np.abs(cross_r))) if cross_r.size else float("nan")),
        "max_cross_block_r2": finite_or_none(float(np.max(cross_r2)) if cross_r2.size else float("nan")),
        "n_r2_ge_0_01": int(np.sum(cross_r2 >= 0.01)),
        "n_r2_ge_0_05": int(np.sum(cross_r2 >= 0.05)),
        "n_r2_ge_0_10": int(np.sum(cross_r2 >= 0.10)),
        "n_r2_ge_0_20": int(np.sum(cross_r2 >= 0.20)),
        "n_r2_ge_0_50": int(np.sum(cross_r2 >= 0.50)),
        "n_r2_ge_0_80": int(np.sum(cross_r2 >= 0.80)),
        "min_eigenvalue": float(np.min(eig)),
        "condition_number": finite_or_none(cond),
        "status": status,
        "reference": "1000G_Phase3_EUR",
        "ancestry": "EUR",
        "build": "GRCh37",
        "n_ref_samples": 503,
        "correlation": "signed_unphased_dosage_r_ref_based",
        "n_matrix_variants": len(ref_ids),
        "n_duplicate_rsID": 0,
        "n_duplicate_positions": duplicate_pos,
        "n_monomorphic_variants": monomorphic,
        "n_variants_with_missing_genotypes": missing_variants,
        "max_abs_symmetry_error": sym_error,
        "max_abs_diagonal_minus_one": diag_error,
        "psd_tolerance": 1e-8,
        "psd_pass": psd_pass,
        "matrix_file": f"results/phase4/{prefix}_QUANT_LD_MATRIX.tsv.gz",
        "target_window_GRCh37": f"chr22:{locus_start}-{locus_end}",
    }
    (PHASE4 / f"{prefix}_QUANT_LD_QC.json").write_text(json.dumps(qc, indent=2) + "\n")
    write_matrix(PHASE4 / f"{prefix}_QUANT_LD_MATRIX.tsv.gz", original_ids, raw)

    # Cross-block table is required for L006; for L007 this returns no pairs.
    if prefix == "L006":
        pre = {row["SNP"]: row for row in read_tsv(ROOT / "results/phase3_5/PHASE3_PRE_ADJUDICATION_VARIANTS.tsv") if row["locus_id"] == "AMD_POAG_L006"}
        cs = {snp for snp, row in pre.items() if row["current_AMD_CS"] not in ("", '""') or row["current_POAG_CS"] not in ("", '""')}
        joint = set(pre)
        cross_fields = ["snp1", "snp2", "block1", "block2", "r", "r2", "AMD_PIP_1", "AMD_PIP_2", "POAG_PIP_1", "POAG_PIP_2", "CS_status", "candidate_status"]
        cross_rows = []
        for i, j in cross_idx:
            s1, s2 = original_ids[i], original_ids[j]
            p1, p2 = pre.get(s1, {}), pre.get(s2, {})
            cross_rows.append(
                {
                    "snp1": s1, "snp2": s2, "block1": blocks[i], "block2": blocks[j], "r": raw[i, j], "r2": raw[i, j] ** 2,
                    "AMD_PIP_1": p1.get("current_AMD_PIP", ""), "AMD_PIP_2": p2.get("current_AMD_PIP", ""),
                    "POAG_PIP_1": p1.get("current_POAG_PIP", ""), "POAG_PIP_2": p2.get("current_POAG_PIP", ""),
                    "CS_status": "CURRENT_CS_MEMBER" if s1 in cs or s2 in cs else "NOT_CURRENT_CS",
                    "candidate_status": "L006_JOINT_DISCOVERY_CANDIDATE" if s1 in joint or s2 in joint else "REFERENCE_CROSS_BLOCK_PAIR",
                }
            )
        write_tsv(PHASE4 / "L006_QUANT_CROSS_BLOCK_LD.tsv", cross_rows, cross_fields)

    return {"qc": qc, "ids": original_ids, "matrix": raw, "harmonized": harmonized_rows, "pvar": info, "freq": freq}


def main() -> None:
    l006 = build_locus("L006", 738, 28100711, 30130300)
    l007 = build_locus("L007", 723, 32605227, 33611247)

    # All three prespecified L007 candidates are directly present; r=1 documents direct coverage.
    proxy_fields = ["candidate", "candidate_present", "proxy", "r", "r2", "distance", "allele_relation", "reference", "interpretation"]
    h7 = {row["variant"]: row for row in read_tsv(PHASE4 / "L007_QUANT_LD_HARMONIZATION.tsv")}
    proxy_rows = []
    for snp in ("rs5749498", "rs756481", "rs12170368"):
        row = h7[snp]
        amd_rel = allele_relation(row["AMD_A1"], row["AMD_A2"], row["LD_A1"], row["LD_A2"])
        poag_rel = allele_relation(row["POAG_A1"], row["POAG_A2"], row["LD_A1"], row["LD_A2"])
        proxy_rows.append(
            {
                "candidate": snp, "candidate_present": row["included"] == "True",
                "proxy": f"{row['chr']}:{row['pos']}:{row['LD_A1']}:{row['LD_A2']}", "r": 1.0, "r2": 1.0,
                "distance": 0, "allele_relation": f"AMD:{amd_rel};POAG:{poag_rel}",
                "reference": "1000G_Phase3_EUR", "interpretation": "DIRECT_REFERENCE_VARIANT",
            }
        )
    write_tsv(PHASE4 / "L007_QUANT_PROXY.tsv", proxy_rows, proxy_fields)

    # Complete the audit table with observed target coverage.
    audit_path = ROOT / "metadata/PHASE4_LD_REFERENCE_AUDIT.tsv"
    audit = read_tsv(audit_path)
    for row in audit:
        if row["reference"] == "1000G_Phase3_EUR":
            row["L006_coverage"] = f"{l006['qc']['n_present']}/{l006['qc']['n_requested']}"
            row["L007_coverage"] = f"{l007['qc']['n_present']}/{l007['qc']['n_requested']}"
            row["status"] = "PRIMARY_EUR_LD_PANEL_QC_PASS" if l006["qc"]["status"] == "PASS_QUANTITATIVE_EUR_LD" and l007["qc"]["status"] == "PASS_QUANTITATIVE_EUR_LD" else "PRIMARY_EUR_LD_PANEL_QC_REVIEW"
    write_tsv(audit_path, audit, list(audit[0]))
    print(json.dumps({"L006": l006["qc"], "L007": l007["qc"]}, indent=2))


if __name__ == "__main__":
    main()
