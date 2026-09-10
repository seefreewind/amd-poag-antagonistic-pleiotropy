# AMD–POAG direction-resolved genetic analysis

This repository contains the reproducibility and manuscript-support package for the frozen AMD–POAG antagonistic genetic pleiotropy project.

The project evaluates whether age-related macular degeneration (AMD) and primary open-angle glaucoma (POAG) show opposing genetic architecture. The final interpretation separates three evidence levels:

1. genome-wide genetic covariance;
2. shared-signal support at a locus; and
3. harmonised effect direction of the shared signal.

A negative genome-wide genetic correlation is not treated as proof of locus-level antagonistic pleiotropy. The final frozen evidence includes one candidate opposite-effect shared signal (L006) and one concordant shared-signal contrast (L007).

## Repository contents

- `scripts/`: Phase 4 analysis, figure-generation and manuscript-generation code.
- `config/`: final analysis freeze and prespecified interpretation gate.
- `metadata/`: GWAS provenance, dataset comparison and LD-reference audit tables.
- `results/`: compact machine-readable summaries, figure source data and publication figures.
- `manuscript/`: Human Genetics manuscript package, supplementary structure and claim audit.
- `reports/`: final decision record and locked paper story.

## Data policy

This repository intentionally excludes raw GWAS summary statistics, restricted source data, 1000 Genomes reference genotypes, HDL-L reference files, large LD matrices, cached downloads and intermediate binary objects. Source datasets remain governed by their original providers and should be obtained from the public URLs and citations recorded in `metadata/GWAS_MANIFEST.tsv`.

The uploaded results are derived summary outputs needed to audit the frozen manuscript claims. They do not constitute an independent replication dataset.

## Frozen primary results

- Primary no-MHC LDSC Advanced AMD × POAG: `rg = -0.1798`, `SE = 0.0665`, `P = 0.0068`, `BH-FDR = 0.0113`.
- Rescue LDSC: `rg = -0.164`, `SE = 0.067`, `P = 0.0143`.
- L006: candidate opposite-effect shared signal; unified-coloc `PP4 = 0.975590`.
- L007: concordant shared-signal contrast; unified-coloc `PP4 = 0.967815`.

These statements are constrained by `config/FINAL_ANALYSIS_FREEZE_v1.yaml` and `reports/FINAL_ANALYSIS_DECISION.md`. No Phase 0–3.5 analysis is to be rerun as part of the manuscript revision.

## Reproducibility note

The summary outputs and figures can be inspected without downloading the excluded source datasets. Full re-execution requires the cited source summary statistics, compatible software versions and the external reference resources described in the metadata and supplementary methods.

The archived reproducibility release is available on Zenodo: [DOI 10.5281/zenodo.22689068](https://doi.org/10.5281/zenodo.22689068).

## License and use

The source datasets retain the licences and access conditions of their original providers. Code and derived summaries are shared for research audit and reproducibility; a project-level software/data licence should be added by the authors before public release.
