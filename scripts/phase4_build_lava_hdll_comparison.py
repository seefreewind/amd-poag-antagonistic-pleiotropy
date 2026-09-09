#!/usr/bin/env python3
"""Compare the two-phenotype LAVA result with pre-existing HDL-L blocks."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/phase4"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def as_float(value: str) -> float | None:
    try:
        x = float(value)
        return x if x == x else None
    except (TypeError, ValueError):
        return None


def overlap(a: int, b: int, c: int, d: int) -> tuple[int, int] | None:
    start, stop = max(a, c), min(b, d)
    return (start, stop) if start <= stop else None


def main() -> None:
    hdl = {
        int(r["piece"]): r
        for r in read_tsv(ROOT / "results/phase2/HDLL_LOCAL_RG.tsv")
        if r["Trait1"] == "ADV_AMD" and r["Trait2"] == "POAG" and r["chr"] == "22"
    }
    lava_rows = {r["locus"]: r for r in read_tsv(OUT / "lava/LAVA_BIVARIATE.tsv")}
    blocks = {
        12: (27953418, 29454477),
        13: (29457622, 30961645),
        15: (31905703, 32657397),
        16: (32663153, 33501556),
        17: (33501743, 34361131),
    }
    loci = {
        "L006": (28100711, 30130300, (12, 13)),
        "L007": (32605227, 33611247, (15, 16, 17)),
    }
    fields = [
        "locus", "locus_start", "locus_stop", "hdl_piece", "hdl_start", "hdl_stop", "overlap_start", "overlap_stop",
        "hdl_rg", "hdl_p", "hdl_lower", "hdl_upper", "lava_rho", "lava_p", "lava_lower", "lava_upper",
        "direction_comparison", "interpretation",
    ]
    rows: list[dict[str, object]] = []
    for locus, (start, stop, pieces) in loci.items():
        lava = lava_rows[locus]
        for piece in pieces:
            h = hdl[piece]
            ov = overlap(start, stop, blocks[piece][0], blocks[piece][1])
            hdl_rg = as_float(h["Genetic_Correlation"])
            lava_rho = as_float(lava["rho"])
            same_direction = "NA"
            if hdl_rg is not None and lava_rho is not None:
                same_direction = "SAME_SIGN" if hdl_rg * lava_rho >= 0 else "OPPOSITE_SIGN"
            if hdl_rg is None:
                interpretation = "HDL_L_NOT_ESTIMABLE_IN_BLOCK"
            elif lava_rho is None:
                interpretation = "LAVA_NOT_ESTIMABLE_IN_LOCUS"
            else:
                interpretation = "DIRECTIONALLY_CONCORDANT" if same_direction == "SAME_SIGN" else "DIRECTIONALLY_DISCORDANT"
            rows.append(
                {
                    "locus": locus, "locus_start": start, "locus_stop": stop, "hdl_piece": piece,
                    "hdl_start": blocks[piece][0], "hdl_stop": blocks[piece][1],
                    "overlap_start": ov[0] if ov else "", "overlap_stop": ov[1] if ov else "",
                    "hdl_rg": hdl_rg if hdl_rg is not None else "NA", "hdl_p": as_float(h["P"]) if as_float(h["P"]) is not None else "NA",
                    "hdl_lower": as_float(h["Lower_bound_rg"]) if as_float(h["Lower_bound_rg"]) is not None else "NA",
                    "hdl_upper": as_float(h["Upper_bound_rg"]) if as_float(h["Upper_bound_rg"]) is not None else "NA",
                    "lava_rho": lava_rho if lava_rho is not None else "NA", "lava_p": as_float(lava["p"]) if as_float(lava["p"]) is not None else "NA",
                    "lava_lower": as_float(lava["rho.lower"]) if as_float(lava["rho.lower"]) is not None else "NA",
                    "lava_upper": as_float(lava["rho.upper"]) if as_float(lava["rho.upper"]) is not None else "NA",
                    "direction_comparison": same_direction, "interpretation": interpretation,
                }
            )
    with (OUT / "LAVA_HDLL_COMPARISON.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        writer.writeheader(); writer.writerows(rows)


if __name__ == "__main__":
    main()
