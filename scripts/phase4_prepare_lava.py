#!/usr/bin/env python3
"""Prepare auditable two-phenotype LAVA inputs from the Phase 4 EUR reference."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE4 = ROOT / "results/phase4"
OUT = PHASE4 / "lava_inputs"
OUT.mkdir(parents=True, exist_ok=True)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_text(path: Path, text: str) -> None:
    path.write_text(text)


def prepare_locus(locus: str, start: int, stop: int) -> dict[str, object]:
    rows = [r for r in read_tsv(PHASE4 / f"{locus}_QUANT_LD_HARMONIZATION.tsv") if r["included"] == "True"]
    rows.sort(key=lambda r: (int(r["pos"]), r["variant"]))
    update = []
    snps = []
    for row in rows:
        old = f"{row['chr']}:{row['pos']}:{row['LD_A1']}:{row['LD_A2']}"
        update.append(f"{old}\t{row['variant']}\n")
        snps.append(row["variant"])
    write_text(OUT / f"{locus}_UPDATE_NAME.tsv", "".join(update))
    write_text(OUT / f"{locus}_SNPS.txt", "\n".join(snps) + "\n")
    return {"locus": locus, "start": start, "stop": stop, "n_reference_variants": len(rows), "snps": snps}


def main() -> None:
    l006 = prepare_locus("L006", 28100711, 30130300)
    l007 = prepare_locus("L007", 32605227, 33611247)
    input_info = (
        "phenotype\tcases\tcontrols\tfilename\n"
        "AMD\t15616\t16723\tdata/processed/phase2_5/ADV_AMD_RESCUE_GRCh37.hm3_noMHC.tsv.gz\n"
        "POAG\t16677\t199580\tdata/processed/standardized/POAG.hm3_noMHC.tsv.gz\n"
    )
    write_text(OUT / "PHASE4_LAVA_INPUT.info", input_info)
    loci = [
        f"L006\t22\t28100711\t30130300\t{';'.join(l006['snps'])}\n",
        f"L007\t22\t32605227\t33611247\t{';'.join(l007['snps'])}\n",
    ]
    write_text(OUT / "PHASE4_LAVA_LOCI.txt", "LOC\tCHR\tSTART\tSTOP\tSNPS\n" + "".join(loci))
    manifest = {
        "software": "LAVA",
        "software_source": "https://github.com/josefin-werme/LAVA",
        "reference": "1000G_Phase3_EUR",
        "reference_build": "GRCh37",
        "reference_samples": 503,
        "phenotypes": ["AMD", "POAG"],
        "sample_overlap_file": None,
        "loci": [l006, l007],
        "note": "Only Advanced AMD rescue and overall POAG are analysed; no POAG component or additional phenotype is included.",
    }
    (OUT / "PHASE4_LAVA_INPUT_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"L006": l006["n_reference_variants"], "L007": l007["n_reference_variants"]}, indent=2))


if __name__ == "__main__":
    main()
