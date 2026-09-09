# Supplementary structure for Human Genetics

The supplementary package should be submitted as online resources linked to the main Research Article. The structure below preserves the frozen analysis boundary and moves implementation details out of the main text.

## Online Resource 1 | Supplementary Methods

`HUMAN_GENETICS_SUPPLEMENTARY_METHODS.md` converted to the journal’s supplementary document format. It contains data provenance, harmonization, model parameters, reference-panel QC, reproducibility records and the explicit no-rerun boundary.

## Online Resource 2 | GWAS dataset manifest

Full version of `metadata/GWAS_MANIFEST.tsv`, including public source identifiers, sample counts, genome builds, download status and file checksums.

## Online Resource 3 | Frozen analysis and decision records

`config/FINAL_ANALYSIS_FREEZE_v1.yaml`, `reports/FINAL_ANALYSIS_DECISION.md`, `reports/phase4/PHASE4_STATUS.md` and `reports/phase4/PAPER_STORY_LOCK.md`.

## Online Resource 4 | Global LDSC matrix

Frozen pairwise no-MHC LDSC estimates, standard errors, P values, BH-FDR values, intercept diagnostics and SNP counts for the phenotype matrix.

## Online Resource 5 | HDL-L block-level output

All 2,463 predefined blocks, finite-estimate flags, local estimates, intervals, P values and BH-FDR values. The 696 finite estimates and minimum finite BH-FDR are reported in the main text.

## Online Resource 6 | cFDR discovery output

Variant-level cFDR results and threshold metadata.

## Online Resource 7 | PLACO discovery output

Variant-level PLACO results and threshold metadata.

## Online Resource 8 | Shared discovery intersection

The 41 cFDR–PLACO intersection variants and their frozen locus assignments.

## Online Resource 9 | Phase 3.5 locus evidence table

The seven-locus pre-Phase-4 evidence table, including direction, block-level PP4, CS overlap and historical technical classifications.

## Online Resource 10 | L006 quantitative-LD QC

Coverage, allele audit, positive-semidefinite diagnostics and cross-block LD summary for the L006 GRCh37 window.

## Online Resource 11 | L007 quantitative-LD QC

Coverage, allele audit, positive-semidefinite diagnostics and candidate proxy audit for the L007 GRCh37 window.

## Online Resource 12 | Unified SuSiE and coloc.susie outputs

Aligned variant lists, signal summaries, credible sets, PP4 summaries and the direction re-audit for L006 and L007.

## Online Resource 13 | LAVA output

Frozen L006 and L007 local-correlation estimates, confidence intervals, P values, reference-panel metadata and seed.

## Online Resource 14 | L006 locus-removal LDSC sensitivity

Input removal record and comparison of the rescue estimate before and after removal of L006.

## Online Resource 15 | Figure source data

Machine-readable source data for Figures 1–6 and the figure-generation script. Figures are presentation products of frozen results, not new analyses.

## Online Resource 16 | Claim–evidence audit

`HUMAN_GENETICS_CLAIM_AUDIT.tsv`, including the language gate and required author confirmations.

## Online Resource 17 | Reproducibility and checksums

Software versions, random seed, command records and SHA256 hashes for the final freeze artifacts.

## Online Resource 18 | Supplementary table index

An index of all online tables and their relationship to the main tables. No new biological analyses or additional loci are included in the supplementary package.
