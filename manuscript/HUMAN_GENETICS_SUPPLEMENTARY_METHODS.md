# Supplementary Methods

## 1. Analysis boundary and authoritative records

The analysis was conducted under `config/FINAL_ANALYSIS_FREEZE_v1.yaml`, with the final decision recorded as `CONDITIONAL_GO`. The freeze preserves the upstream Phase 0–3.5 analyses and restricts Phase 4 to quantitative European LD rescue and final adjudication of L006 and L007. No Phase 0–3.5 analysis was rerun. No genome-wide cFDR, genome-wide PLACO, discovery SuSiE/coloc, single-cell, multiome, eQTL, TWAS, Mendelian randomization, pathway or drug-target expansion was added during manuscript preparation. The figure revisions are presentation changes only.

Historical intermediate values were not used when they differed from the final freeze. The final technical labels are retained for auditability, but the main manuscript uses human-facing evidence categories: candidate opposite-effect shared signal, opposite-direction shared discovery locus and concordant shared signal.

## 2. Data provenance, ancestry and sample overlap

The primary Advanced AMD summary statistics were the European IAMDGC resource reported by Fritsche *et al.* and contained 16,144 cases and 17,832 controls. The public file provided P values, sample-size information and an overall direction field but no reliable per-variant beta, standard error, allele frequency or INFO field. It was therefore used as a signed-Z input and was not converted into beta/standard-error estimates.

The Advanced AMD rescue resource was the European subset of the IAMDGC 2.0 resource reported by Gorski *et al.* It contained 15,616 cases and 16,723 controls and supplied beta and standard-error fields. The source coordinates were standardised to GRCh37 after liftover. The rescue resource is related to the primary AMD programme and was used for rescue LDSC and the Phase 4 locus-level analyses; it was not treated as an independent replication cohort.

The primary POAG summary statistics were the European meta-analysis reported by Gharahkhani *et al.* and contained 16,677 cases and 199,580 controls. The POAG non-IOP and IOP component resources each contained 14,853 cases and 106,544 controls and were derived from the GWAS-by-subtraction framework. They are statistically dependent decompositions of POAG and were not treated as independent cohorts. Early AMD was retained in the frozen phenotype matrix. The available NTG resource was multi-ancestry and lacked an analysis-ready European-only subset; it was used as context only.

All primary analyses used European-ancestry summary statistics and GRCh37 coordinates. The sample-overlap audit could not reconstruct participant-level overlap from the public files. Unknown overlap was not treated as measured zero overlap. No explicit sample-overlap matrix was supplied to LAVA.

## 3. Harmonization and quality control

Standardized inputs were restricted to autosomes 1–22, valid genomic positions and valid allele pairs. Duplicate variants and invalid allele records were removed. Ambiguous A/T and C/G variants were excluded when frequency information could not resolve strand orientation. Where source fields were available, INFO was required to be at least 0.80 and MAF at least 0.01. LDSC inputs were intersected with the project HapMap3 SNP list. The primary LDSC analysis excluded the GRCh37 MHC interval on chromosome 6 from 25,000,000 to 34,000,000 bp.

Effects were retained in source orientation during standardisation and harmonised to the reference allele orientation of each locus-specific LD matrix. Allele swaps changed the sign of beta and Z values. Complement and complement-swapped configurations were handled when unambiguous. Variants with unresolved allele or build orientation were excluded from locus-level adjudication. For the signed-Z Advanced AMD primary file, beta and standard errors were not back-calculated.

For direction classification, the product of harmonised Advanced AMD and POAG effects was used. A negative product was classified as opposite direction and a positive product as concordant direction. This is a summary-statistics direction classification and does not by itself distinguish biological pleiotropy from LD-mediated correlated association.

## 4. Genome-wide LDSC and HDL-L

LDSC was applied to HapMap3-filtered summary statistics. The primary Advanced AMD–POAG estimate used no-MHC inputs. Observed-scale SNP heritability, the cross-trait estimate, intercept diagnostics and standard errors were retained. Liability-scale conversion was not performed because suitable population-prevalence information was not available. Major-locus sensitivity removed APOE, ARMS2/HTRA1 and CFH. Leave-one-chromosome-out analyses excluded each chromosome in turn. The primary pairwise BH-FDR was calculated within the frozen 10-pair no-MHC phenotype matrix.

HDL-L was applied to 2,463 predefined blocks. The output was retained without imputing missing local estimates. Of the tested blocks, 696 estimates were finite. The minimum finite BH-FDR was 0.3007, and no block reached BH-FDR < 0.05. The working N0 = 0 setting in the documented HDL-L workflow is a modelling assumption and not evidence that the contributing studies had no participant overlap.

## 5. Cross-trait discovery and frozen locus set

The discovery stage combined pleiotropy-informed cFDR and PLACO. The frozen thresholds were conjunctional cFDR ≤ 0.05 and PLACO P ≤ 5 × 10−8. The intersection of the two outputs was used as high-specificity shared-locus discovery evidence. It contained 41 variants grouped into seven prespecified locus windows. The discovery counts were 44 cFDR variants, 259 PLACO variants, five opposite-direction loci and two concordant loci. The intersection and locus assignments were frozen before Phase 4.

## 6. Quantitative EUR LD reference and Phase 4 QC

Phase 4 used the 1000 Genomes Phase 3 European reference panel, comprising 503 samples and GRCh37 coordinates. Signed pairwise LD was computed from reference dosages after allele harmonisation. Matrices were audited for variant coverage, allele consistency, positive semidefiniteness and cross-block quantitative LD.

For L006, the expanded window was chr22:28,100,711–30,130,300. The reference contained 737 of 738 requested variants, corresponding to coverage 0.99864498645. The maximum cross-block absolute correlation was 0.50923044834 and the maximum cross-block r² was 0.25931564952. No cross-block pair had r² ≥ 0.50. For L007, the reference contained 720 of 723 requested variants, corresponding to coverage 0.9958506224. The prespecified candidate proxy audit had r² = 1 for the relevant direct candidates. Both matrices passed the project QC criterion.

## 7. Multi-signal fine-mapping and colocalization

Fine-mapping used SuSiE through `coloc::runsusie` with `susieR` version 0.14.2. Both traits were aligned to the same reference-oriented variant order and the same quantitative EUR LD matrix. The frozen configuration allowed a maximum of 10 single-effect signals, used 95% credible-set coverage, prior variance 50, a maximum of 100 iterations and convergence tolerance 0.001, with residual-variance estimation disabled. Credible-set overlap was summarised at the signal level.

Colocalization used `coloc.susie` version 5.2.3 with p1 = 1 × 10−4, p2 = 1 × 10−4 and p12 = 1 × 10−5. PP4 ≥ 0.80 was prespecified as strong shared-signal support in the technical framework. The reported PP4 is the strongest signal-pair posterior within the unified analysis. Signal-level credible-set overlap and PP4 describe a shared-signal configuration under the model; neither establishes a shared causal variant.

L006 used 721 aligned variants. The Advanced AMD fit had one signal and a 24-variant credible set; the POAG fit had three signals. L007 used 705 aligned variants. The Advanced AMD fit had three signals and the POAG fit had one signal. Both traits converged at both loci.

## 8. L006 and L007 direction adjudication

The same Phase 4 workflow was applied to L006 and L007. For L006, PP4 was 0.975590102089367 and signal-level credible sets overlapped at 10 variants. The top shared variant was rs1547014, with opposite harmonised Advanced AMD and POAG effects. For L007, PP4 was 0.967815315878016 and signal-level credible sets overlapped at three variants. The top shared variant was rs5749498, with concordant harmonised effects. The final evidence categories were therefore candidate opposite-effect shared signal for L006 and concordant shared-signal contrast for L007.

## 9. LAVA sensitivity analysis

LAVA version 0.1.5 was used only for L006 and L007, using Advanced AMD rescue and overall POAG. The reference was 1000 Genomes Phase 3 EUR with 503 samples. The fixed project seed was 20260909. The documented settings included minimum K = 2, pruning threshold 99, maximum retained proportion K = 0.75 and maximum block size 3,000, with adaptive P-value thresholds of 1 × 10−4 and 1 × 10−6 and confidence intervals. No explicit sample-overlap matrix was supplied. LAVA was treated as local-correlation sensitivity using the same summary statistics, not as independent replication.

The frozen L006 estimate was rho = −0.331961, 95% CI −0.78294 to 0.05909, P = 0.0941787. The frozen L007 estimate was rho = 0.0671874, 95% CI −0.22246 to 0.36139, P = 0.639564. The overlapping HDL-L estimates were retained as contextual results and were not treated as an independent test of the LAVA findings.

## 10. Reproducibility and software

The computational environment used R 4.4.x, Python 3.9.6, `susieR` 0.14.2, `coloc` 5.2.3, LAVA 0.1.5 and PLINK2 2.0.0-a.7.3 M1 (8 August 2026). The LAVA source commit was `e729a245f7b6923967a96804fbf5246eadf2d6c6`. The project seed was 20260909. Phase 4 source files, scripts, command records, frozen YAML configuration and SHA256 checksums are retained in the project directory.

The final freeze artifact hashes include: `LAVA_BIVARIATE.tsv`, `65f3a8706eae28cc6015af7357f1b053970d3fd904860d0fece18166139704c7`; `FINAL_ANTAGONISTIC_TIER_TABLE_PHASE4.tsv`, `17d30cbacdd67e58c950560fb5248bd98f08cefef7da2d9f64c1b83d3a7c4171`; L006 quantitative-LD QC, `6dfea3775dd9398cf6685fd231b4e28ad0db40c4c7428ec922d77a40f4966747`; L007 quantitative-LD QC, `5851f744cea727b66d2c2a2cd229a179090eeb9d8e1c4861922cee7261ce2c8e`; L006 unified coloc, `0dd8b0a89e91651977a21b61507fb7c8212b47338d82217f41b9777624021d6c`; and L007 unified coloc, `02a8c83ab9c5dcf425b2dab97f39631a8d282205804672ea1f4aac703823085d`.

The public code repository and accession remain author inputs. The authors should also confirm the journal-compliant disclosure wording for any AI-assisted editorial tools used during manuscript preparation. No AI-assisted tool was used to generate, alter or interpret the frozen numerical results.
