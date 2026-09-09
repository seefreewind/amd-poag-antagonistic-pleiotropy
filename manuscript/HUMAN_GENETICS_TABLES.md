# Main tables

## Table 1 | GWAS datasets and analytical roles

| Dataset | Phenotype or component | Ancestry | Cases | Controls | Total N | Build | Effect-size status | Role in this study |
|---|---|---:|---:|---:|---:|---|---|---|
| Advanced AMD primary | Advanced AMD (GA and/or CNV) | European | 16,144 | 17,832 | 33,976 | GRCh37 | Signed-Z input; reliable beta/SE unavailable | Primary LDSC and frozen discovery input |
| Advanced AMD rescue | Advanced AMD, full-effect rescue resource | European | 15,616 | 16,723 | 32,339 | GRCh37 after liftover | Beta and SE available | Rescue LDSC, fine-mapping and LAVA; not independent replication |
| Early AMD | Early AMD by fundus photography | European | 14,034 | 91,214 | 105,248 | GRCh37 | Beta and SE available | Secondary phenotype in frozen matrix |
| POAG | Overall primary open-angle glaucoma | European | 16,677 | 199,580 | 216,257 | GRCh37 | Beta and SE available | Primary POAG input |
| POAG non-IOP component | IOP-independent component from GWAS-by-subtraction | European | 14,853 | 106,544 | 121,397 | Source archive | Component effect fields | Conditional decomposition; statistically dependent on parent POAG |
| POAG IOP component | IOP-dependent component from GWAS-by-subtraction | European | 14,853 | 106,544 | 121,397 | Source archive | Component effect fields | Conditional decomposition; statistically dependent on parent POAG |
| NTG | Normal-tension glaucoma, IGGC stage 2 | Multi-ancestry source; EUR subgroup pending | 7,942 | 384,431 | 392,373 | Source archive | Final ancestry/build audit pending | Sensitivity context only |

AMD, age-related macular degeneration; CNV, choroidal neovascularization; GA, geographic atrophy; IGGC, International Glaucoma Genetics Consortium; IOP, intraocular pressure; NTG, normal-tension glaucoma; POAG, primary open-angle glaucoma. Dataset provenance and access metadata are retained in `metadata/GWAS_MANIFEST.tsv`. The rescue resource is related to the primary Advanced AMD programme and was not treated as an independent replication cohort

## Table 2 | Global genetic correlation and robustness analyses

| Analysis | N SNPs or scope | rg | SE | P value | BH-FDR | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Primary no-MHC LDSC: Advanced AMD × POAG | 1,172,447 HapMap3 SNPs | −0.1798 | 0.0665 | 0.0068 | 0.0113 | Negative genome-wide genetic relationship |
| Rescue LDSC: Advanced AMD rescue × POAG | 1,126,966 SNPs | −0.1640 | 0.0670 | 0.0143 | — | Same direction; full-effect rescue resource |
| Primary minus APOE | 1,171,993 SNPs | −0.1750 | 0.0636 | 0.0059 | — | Direction retained |
| Primary minus ARMS2/HTRA1 | 1,171,260 SNPs | −0.1906 | 0.0835 | 0.0225 | — | Direction retained |
| Primary minus CFH | 1,171,291 SNPs | −0.2316 | 0.0549 | 2.46 × 10−5 | — | Direction retained |
| LOCO range across chromosomes 1–22 | Chromosome-exclusion analyses | −0.2209 to −0.1659 | — | — | — | All estimates remained negative |
| Rescue LDSC minus L006 | Locus-removal sensitivity | −0.1620 | 0.0666 | 0.0150 | — | Δrg = 0.002 from the original rescue estimate |
| HDL-L local scan | 2,463 predefined blocks; 696 finite estimates | — | — | — | 0.3007 minimum finite BH-FDR | No block reached BH-FDR < 0.05 |

BH-FDR, Benjamini–Hochberg false-discovery rate; HDL-L, high-definition likelihood; LDSC, linkage disequilibrium score regression; LOCO, leave-one-chromosome-out; MHC, major histocompatibility complex; rg, genetic correlation; SE, standard error. The primary LDSC BH-FDR was computed within the frozen 10-pair no-MHC phenotype matrix. Liability-scale conversion was not performed

## Table 3 | Shared loci, direction, fine-mapping support and final evidence category

| Locus | Interval (GRCh37) | Discovery direction | Joint discovery variants | Opposite / concordant | Phase 4 LD coverage | Unified PP4 | Signal CS overlap | Top shared variant | Final direction | LAVA rho (P) | Final evidence category |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| L001 | chr2:227,585,593–228,587,187 | Opposite | 3 | 3 / 0 | Not run; Phase 3.5 retained | — | 0 | rs11884770 / rs11678528 | Opposite | — | Opposite-direction shared discovery locus |
| L002 | chr6:50,303,050–51,405,067 | Opposite | 5 | 5 / 0 | Not run; Phase 3.5 retained | — | 0 | rs987237 | Opposite | — | Opposite-direction shared discovery locus |
| L003 | chr9:21,497,872–22,625,347 | Opposite | 24 | 24 / 0 | Not run; Phase 3.5 retained | — | 0 | rs10811650 / rs7865618 | Opposite | — | Opposite-direction shared discovery locus |
| L004 | chr14:60,572,875–61,572,875 | Opposite | 1 | 1 / 0 | Not run; Phase 3.5 retained | — | 0 | rs10483727 | Opposite | — | Opposite-direction shared discovery locus |
| L005 | chr19:44,895,619–45,922,946 | Concordant | 2 | 0 / 2 | Not run; Phase 3.5 retained | — | 0 | rs2075650 | Concordant | — | Concordant shared discovery locus |
| L006 | chr22:28,100,711–30,130,300 | Opposite | 3 | 3 / 0 | 737/738 (0.998645) | 0.975590 | 10 | rs1547014 | Opposite | −0.331961 (0.0941787) | Candidate opposite-effect shared signal |
| L007 | chr22:32,605,227–33,611,247 | Concordant | 3 | 0 / 3 | 720/723 (0.995851) | 0.967815 | 3 | rs5749498 | Concordant | 0.0671874 (0.639564) | Concordant shared-signal contrast |

CS, credible set; LD, linkage disequilibrium; LAVA, Local Analysis of [co]Variant Association; PP4, posterior probability for a shared causal configuration under the coloc.susie model. L001–L005 retain their frozen Phase 3.5 classifications. L006 and L007 used the same Phase 4 quantitative EUR LD and unified SuSiE/coloc.susie workflow. For L006, maximum cross-block |r| = 0.5092, maximum cross-block r² = 0.2593 and no cross-block pair had r² ≥ 0.50. For L007, the final matrix passed QC and the direct candidate proxy audit had r² = 1. A PP4 value and credible-set overlap describe shared-signal support; they do not establish a shared causal variant
