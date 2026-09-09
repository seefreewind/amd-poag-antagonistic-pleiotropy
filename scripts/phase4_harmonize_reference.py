#!/usr/bin/env python3
"""Harmonize frozen GWAS variants to the quantitative 1000G EUR reference."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE4 = ROOT / "results/phase4"
PVAR = PHASE4 / "1000G_chr22_L006_L007_EUR_IDS.pvar"


def complement(allele: str) -> str:
    return allele.translate(str.maketrans("ACGT", "TGCA"))


def relation(a1: str, a2: str, ref: str, alt: str) -> str:
    if a1 == ref and a2 == alt:
        return "exact"
    if a1 == alt and a2 == ref:
        return "swapped"
    if complement(a1) == ref and complement(a2) == alt:
        return "complement"
    if complement(a1) == alt and complement(a2) == ref:
        return "complement_swapped"
    return "mismatch"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def read_pvar(path: Path) -> dict[int, list[dict[str, str]]]:
    by_pos: dict[int, list[dict[str, str]]] = {}
    with path.open() as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            chrom, pos, vid, ref, alt, *_ = line.rstrip("\n").split("\t")
            by_pos.setdefault(int(pos), []).append(
                {"chrom": chrom, "pos": pos, "id": vid, "ref": ref, "alt": alt}
            )
    return by_pos


def harmonize(rows: list[dict[str, str]], by_pos: dict[int, list[dict[str, str]]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        pos = int(row["BP"])
        matches = []
        for refrow in by_pos.get(pos, []):
            rel_a = relation(row["AMD_A1"], row["AMD_A2"], refrow["ref"], refrow["alt"]) if row["AMD_present"] == "True" else "mismatch"
            rel_p = relation(row["POAG_A1"], row["POAG_A2"], refrow["ref"], refrow["alt"]) if row["POAG_present"] == "True" else "mismatch"
            rel = rel_a if rel_a != "mismatch" else rel_p
            if rel != "mismatch":
                matches.append((refrow, rel_a, rel_p, rel))
        refrow, rel_a, rel_p, rel = matches[0] if matches else ({}, "mismatch", "mismatch", "mismatch")
        included = bool(matches)
        out.append(
            {
                "SNP": row["SNP"],
                "chr": row["CHR"],
                "pos": row["BP"],
                "AMD_A1": row["AMD_A1"],
                "AMD_A2": row["AMD_A2"],
                "POAG_A1": row["POAG_A1"],
                "POAG_A2": row["POAG_A2"],
                "LD_ID": refrow.get("id", ""),
                "LD_A1": refrow.get("ref", ""),
                "LD_A2": refrow.get("alt", ""),
                "AMD_beta": row["AMD_beta"],
                "POAG_beta": row["POAG_beta"],
                "AMD_relation": rel_a,
                "POAG_relation": rel_p,
                "allele_status": "PASS" if included else "MISSING_REFERENCE",
                "included": included,
            }
        )
    return out


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    by_pos = read_pvar(PVAR)
    common_fields = [
        "SNP", "chr", "pos", "AMD_A1", "AMD_A2", "POAG_A1", "POAG_A2", "LD_ID",
        "LD_A1", "LD_A2", "AMD_beta", "POAG_beta", "AMD_relation", "POAG_relation",
        "allele_status", "included",
    ]
    outputs: dict[str, list[dict[str, object]]] = {}
    for locus in ("L006", "L007"):
        rows = harmonize(read_tsv(PHASE4 / f"{locus}_REQUESTED_VARIANTS.tsv"), by_pos)
        outputs[locus] = rows
        write_tsv(PHASE4 / f"{locus}_QUANT_LD_HARMONIZATION.tsv", rows, common_fields)
        ids = [str(row["LD_ID"]) for row in rows if row["included"]]
        (PHASE4 / f"{locus}_REFERENCE_IDS.txt").write_text("\n".join(ids) + ("\n" if ids else ""))

    candidates = {row["SNP"]: row for row in outputs["L007"]}
    proxy_fields = ["candidate", "candidate_present", "proxy", "r", "r2", "distance", "allele_relation", "reference", "interpretation"]
    proxy_rows = []
    for snp in ("rs5749498", "rs756481", "rs12170368"):
        row = candidates[snp]
        proxy_rows.append(
            {
                "candidate": snp,
                "candidate_present": row["included"],
                "proxy": row["LD_ID"] if row["included"] else "",
                "r": "",
                "r2": "",
                "distance": 0 if row["included"] else "",
                "allele_relation": f"AMD:{row['AMD_relation']};POAG:{row['POAG_relation']}",
                "reference": "1000G_Phase3_EUR",
                "interpretation": "DIRECT_REFERENCE_VARIANT_PENDING_LD_MATRIX" if row["included"] else "CANDIDATE_NOT_PRESENT_AT_ALIGNED_POSITION",
            }
        )
    write_tsv(PHASE4 / "L007_QUANT_PROXY.tsv", proxy_rows, proxy_fields)
    print({locus: {"requested": len(rows), "present": sum(bool(r["included"]) for r in rows)} for locus, rows in outputs.items()})


if __name__ == "__main__":
    main()
