# Direction-resolved genetic analysis of age-related macular degeneration and primary open-angle glaucoma identifies a candidate opposite-effect shared signal

**Authors:** Da Lin¹, Ying Chen², Yue Liu², Yu Zhang¹

**Affiliation 1:** Department of Ophthalmology, The Second Affiliated Hospital of Wenzhou Medical University, No. 109 Xueyuan West Road, Lucheng District, Wenzhou, Zhejiang Province, China

**Affiliation 2:** Wenzhou Medical University, Wenzhou, Zhejiang Province, China

**Corresponding author:** Yu Zhang; email: zhangyu1@wzhealth.com; ORCID: https://orcid.org/0000-0001-8579-3692

## Abstract

### Background

Age-related macular degeneration (AMD) and primary open-angle glaucoma (POAG) may share genetic architecture, but a negative genome-wide genetic correlation does not by itself establish locus-level opposite effects. We separated genome-wide covariance, shared-signal support and harmonized allelic direction in a frozen summary-statistics analysis.

### Methods

European-ancestry genome-wide association study (GWAS) summary statistics were analysed with no-major-histocompatibility-complex (MHC) linkage disequilibrium score regression (LDSC), conditional false-discovery rate (cFDR), pleiotropic analysis under composite null (PLACO), quantitative European linkage disequilibrium, multi-signal fine-mapping, colocalization and Local Analysis of [co]Variant Association (LAVA). Discovery was frozen before locus adjudication.

### Results

The primary Advanced AMD–POAG LDSC estimate was negative (rg = −0.1798, standard error (SE) = 0.0665, P = 0.0068; Benjamini–Hochberg false-discovery rate (BH-FDR) = 0.0113) and remained negative in rescue LDSC (rg = −0.164, P = 0.0143). No local block reached BH-FDR < 0.05. Discovery yielded 44 cFDR variants, 259 PLACO variants, 41 intersection variants and seven loci. L006 showed quantitative linkage-disequilibrium coverage of 737/738 variants, posterior probability for a shared causal configuration (PP4) = 0.9756 and 10 overlapping signal-level credible-set variants; rs1547014 had opposite harmonized effects. L007 showed similarly strong shared-signal support (PP4 = 0.9678; overlap = 3) but concordant effects at rs5749498. LAVA was directionally negative at L006 but not statistically definitive.

### Conclusions

AMD and POAG show a negative genome-wide genetic relationship with heterogeneous locus-level directions. L006 is a candidate opposite-effect shared signal, whereas L007 demonstrates that shared-signal support and opposite direction are separable properties. Independent validation is required.

**Keywords:** age-related macular degeneration; primary open-angle glaucoma; genetic correlation; pleiotropy; fine-mapping; colocalization

## List of abbreviations

AMD, age-related macular degeneration; BH-FDR, Benjamini–Hochberg false-discovery rate; CNV, choroidal neovascularization; CS, credible set; cFDR, conditional false-discovery rate; GA, geographic atrophy; GWAS, genome-wide association study; HDL-L, high-definition likelihood; IOP, intraocular pressure; LD, linkage disequilibrium; LDSC, linkage disequilibrium score regression; LAVA, Local Analysis of [co]Variant Association; LOCO, leave-one-chromosome-out; MHC, major histocompatibility complex; NTG, normal-tension glaucoma; PLACO, pleiotropic analysis under composite null hypothesis; POAG, primary open-angle glaucoma; PP4, posterior probability for a shared causal configuration; rg, genetic correlation; SE, standard error; SNP, single-nucleotide polymorphism; SuSiE, Sum of Single Effects

## Introduction

Age-related macular degeneration and primary open-angle glaucoma are common age-related ocular diseases with distinct principal sites of pathology. AMD affects the macula and retinal pigment epithelium, whereas POAG is characterized by progressive optic-nerve and retinal-ganglion-cell injury, often in the context of altered intraocular pressure. Both diseases are complex, heritable and clinically heterogeneous. Their anatomical distinction makes genetic overlap biologically informative, but it also makes the meaning of overlap difficult to define. A shared genetic signal may reflect common susceptibility, correlated variants in linkage disequilibrium (LD), or effects that point in opposite directions for the two diseases.
The distinction also matters for how cross-disease findings are communicated. Genome-wide covariance can motivate a search for shared biology, while a locus-level result may refine that search. Neither level alone specifies whether the same allele increases risk for both diseases, decreases risk for both, or has opposing reference-oriented effects. A direction-resolved analysis can therefore add interpretability without assuming that statistical sharing is equivalent to a biological mechanism.

Large genome-wide association studies (GWASs) have established extensive polygenic architecture for AMD and POAG. Advanced AMD studies have implicated complement, lipid and other biological regions, while early AMD analyses have identified both shared and stage-specific components of disease susceptibility (Fritsche et al. 2016; Winkler et al. 2020). The updated IAMDGC resource adds full-effect information for an expanded Advanced AMD dataset (Gorski et al. 2025). POAG meta-analysis has identified risk loci across ancestries, and GWAS-by-subtraction has separated IOP-dependent from IOP-independent genetic components (Gharahkhani et al. 2021; Huang et al. 2024). The NTG literature provides additional context for genetically distinct glaucoma components (Diaz-Torres et al. 2024). Earlier cross-trait work reported positive or suggestive AMD–POAG genetic overlap (Cuellar-Partida et al. 2016), whereas a recent multi-ocular analysis reported a negative AMD–POAG genetic correlation within a broader integrative study (Bai et al. 2026). Related analyses have also described pleiotropy across age-related ocular disorders (Yao et al. 2023). These findings establish a relevant cross-disease signal, but they do not resolve its direction at individual shared loci.
The available datasets also differ in ascertainment, disease stage, effect-size availability and statistical dependence. A rescue dataset with full beta and standard-error fields can support fine-mapping that is not possible with a signed-Z primary file, but it does not become an independent replication simply by supplying additional fields. Similarly, statistically derived POAG components can refine phenotype interpretation while remaining dependent on the parent POAG GWAS. Keeping these roles explicit is necessary for a defensible comparison of global and locus-level evidence.

The unresolved statistical distinction is concise: **rg < 0 ≠ locus-level antagonistic pleiotropy**. A negative genome-wide correlation is an aggregate covariance parameter. It may arise from many small opposing effects, a mixture of concordant and discordant loci with unequal magnitudes, or correlated association patterns in regions of complex LD. It does not imply that every shared locus is antagonistic or that the same causal variant influences both traits. Conversely, an opposite-effect shared signal may contribute little to the genome-wide average. Shared association, a shared-signal configuration and opposite allelic direction are therefore separate properties that require separate evidence.
This separation is also important for interpreting colocalization. Posterior support for a shared configuration is conditional on the LD model, input summary statistics and prior specification. A high posterior can coexist with concordant effects, as illustrated by L007, and an opposite direction can be observed without establishing that a single variant is causal. The analysis should therefore be read as an evidence chain with distinct endpoints rather than as a single pleiotropy score.

The primary contribution of this study was not the detection of a negative genetic correlation itself, but the direction-resolved adjudication of shared genetic signals using quantitative LD, multi-signal fine-mapping and colocalization. We combined frozen genome-wide LDSC and HDL-L analyses with cFDR and PLACO discovery, explicit allele-direction harmonization, quantitative 1000 Genomes European LD, unified SuSiE and coloc.susie analyses, and restricted LAVA sensitivity analyses. The strongest opposite-direction locus, L006, was evaluated alongside L007, a similarly supported concordant locus processed under the same Phase 4 workflow. This design was intended to determine whether the AMD–POAG relationship reflects diffuse opposing architecture, discrete opposite-effect shared signals, or a mixture, while preserving the distinction between candidate statistical evidence and biological causality.
The study was designed as an adjudication of already frozen candidates, not as an open-ended search for additional loci. This boundary makes the L006–L007 comparison interpretable: both loci were exposed to the same reference panel, alignment rules, multi-signal model and posterior threshold. The resulting manuscript uses the technical freeze for reproducibility and a separate human-facing terminology layer for interpretation. That terminology is deliberately limited to candidate evidence and does not imply clinical utility, therapeutic relevance or a completed validation programme.

## Methods

### Study design and analysis boundary

This was a staged summary-statistics genetic analysis conducted under the final project freeze `config/FINAL_ANALYSIS_FREEZE_v1.yaml`. Phase 0 established data provenance, ancestry, genome build and quality-control eligibility. Phase 1 estimated genome-wide heritability and genetic correlation. Phase 2 estimated local genetic correlation with HDL-L. Phase 3 used cFDR and PLACO for cross-trait shared-locus discovery, followed by locus-level fine-mapping and colocalization. Phase 3.5 audited direction, LD coverage and technical evidence categories. These upstream stages were frozen before Phase 4.

Phase 4 was restricted to quantitative European LD rescue and final adjudication of L006 and L007. It did not rerun Phase 0–3.5, genome-wide cFDR, genome-wide PLACO or discovery fine-mapping. No single-cell, multiome, eQTL, TWAS, Mendelian randomization, pathway or drug-target analyses were added. The final manuscript follows the freeze and the associated decision record when historical reports contain older intermediate classifications.

### GWAS datasets and phenotype scope

The primary Advanced AMD summary statistics were a European IAMDGC resource containing 16,144 cases and 17,832 controls. The public file supplied association P values, sample-size information and an overall direction field but no reliable per-variant beta, standard error, allele frequency or INFO field. It was therefore used as a signed-Z input for the primary LDSC and frozen discovery analyses; beta and standard errors were not back-calculated.

The Advanced AMD rescue resource was the European subset of the IAMDGC 2.0 resource and contained 15,616 cases and 16,723 controls. It supplied beta and standard-error fields and was standardised to GRCh37 after coordinate liftover. The rescue resource was used for rescue LDSC, locus-level fine-mapping and LAVA. It is related to the primary AMD programme and was not treated as an independent replication cohort.

The primary POAG summary statistics were a European meta-analysis containing 16,677 cases and 199,580 controls. The POAG non-IOP and IOP component datasets each contained 14,853 cases and 106,544 controls and were derived with GWAS-by-subtraction. They were analysed as conditional decompositions and not as independent replication cohorts. Early AMD was retained in the frozen phenotype matrix. The available NTG resource was multi-ancestry and lacked an analysis-ready European-only subset; it was retained as sensitivity context only.

All primary analyses used European-ancestry summary statistics and GRCh37 coordinates. The sample-overlap audit could not reconstruct participant-level overlap from public files. Unknown overlap was not treated as measured zero overlap. Because the POAG component datasets were derived from the parent POAG GWAS, their estimates were interpreted as statistically dependent.

### Harmonization and quality control

Standardized inputs were restricted to autosomes 1–22, valid genomic positions and valid allele pairs. Duplicate variants and invalid allele records were removed. Ambiguous A/T and C/G variants were removed when frequency information could not resolve strand orientation. Where source fields were available, INFO was required to be at least 0.80 and MAF at least 0.01. LDSC inputs were intersected with the project HapMap3 SNP list. The primary LDSC analysis excluded the GRCh37 MHC interval on chromosome 6 from 25,000,000 to 34,000,000 bp.

Effects were retained in source orientation during standardisation and then harmonised to the reference-allele orientation used for each locus-level LD matrix. Allele swaps changed the signs of beta and Z values. Complement and complement-swapped configurations were handled when unambiguous. Variants with unresolved allele or build orientation were excluded from locus-level adjudication. For direction classification, the product of harmonised Advanced AMD and POAG effects was used: a negative product indicated opposite direction and a positive product indicated concordant direction. This classification describes summary-statistics direction and does not distinguish biological pleiotropy from LD-mediated correlated association.
The primary and rescue resources were kept analytically distinct. The primary signed-Z file supported the genome-wide no-MHC result, whereas the rescue file supported analyses requiring full effect-size fields. This separation prevented a reconstructed beta from being mistaken for an observed source quantity and allowed the main text to state clearly which result came from which resource. The final source manifests also retain download status, build information and checksums for audit.

### Genome-wide genetic correlation and local correlation

LDSC was applied to HapMap3-filtered summary statistics. The primary Advanced AMD–POAG estimate used no-MHC inputs. Observed-scale SNP heritability, the cross-trait estimate, intercept diagnostics and standard errors were retained. Liability-scale conversion was not performed because suitable prevalence information was unavailable. Prespecified robustness analyses removed APOE, ARMS2/HTRA1 and CFH and excluded each chromosome in turn. The primary pairwise BH-FDR was computed within the frozen 10-pair no-MHC phenotype matrix.
The no-MHC analysis was treated as the primary global estimate because the MHC contains complex LD and multiple immune-related associations that can disproportionately influence cross-trait covariance. The major-locus exclusions tested whether the sign depended on three established AMD regions, while LOCO analyses tested whether any single chromosome changed the direction. These were robustness analyses of the same global question and were not interpreted as replication cohorts.

HDL-L was applied to 2,463 predefined blocks. Missing estimates were not imputed. Local estimates were interpreted with their block-level uncertainty, local heritability requirements and BH-FDR across the Advanced AMD–POAG scan. The documented HDL-L workflow used N0 = 0 as a working assumption; this was not interpreted as evidence of measured zero sample overlap.

### Cross-trait discovery and locus classification

Cross-trait discovery combined pleiotropy-informed cFDR with PLACO. The frozen thresholds were conjunctional cFDR ≤ 0.05 and PLACO P ≤ 5 × 10−8. The intersection was used as shared-locus discovery evidence, not as evidence of a shared causal variant. Nearby variants were grouped into the seven frozen locus windows. The Phase 3.5 technical framework distinguished opposite-direction loci without validated shared-signal configuration from stronger Phase 4 candidates. The main manuscript translates these labels into human-facing evidence categories and retains technical tiers only in supplementary audit material.
The intersection was not re-ranked after viewing the Phase 4 results. Discovery direction was assigned before quantitative-LD adjudication, and the concordant loci were retained even though they did not support an antagonistic interpretation. This sequencing was intended to reduce the risk that the final story would be defined only by loci with the desired direction.

### Fine-mapping, quantitative LD and colocalization

Locus-level fine-mapping used SuSiE through `coloc::runsusie` and `susieR` version 0.14.2. Phase 4 aligned both traits to the same reference-oriented variant order and quantitative EUR LD matrix. The frozen configuration allowed up to 10 single-effect signals, used 95% credible-set coverage, prior variance 50, a maximum of 100 iterations and convergence tolerance 0.001, with residual-variance estimation disabled.

Phase 4 used the 1000 Genomes Phase 3 European reference panel, comprising 503 samples at GRCh37. Signed pairwise LD was calculated from reference dosages after allele harmonization. The matrices were audited for variant coverage, allele consistency, positive semidefiniteness and cross-block quantitative LD. For L006, the expanded window was chr22:28,100,711–30,130,300. For L007, the window was chr22:32,605,227–33,611,247. Unified SuSiE and coloc.susie were run only after the relevant quantitative-LD QC passed.

Colocalization used `coloc.susie` version 5.2.3 with p1 = 1 × 10−4, p2 = 1 × 10−4 and p12 = 1 × 10−5. PP4 ≥ 0.80 was prespecified as strong shared-signal support within the technical framework. The reported PP4 was the strongest signal-pair posterior, together with signal-level credible-set overlap. These quantities describe a shared-signal configuration under the model and do not establish a shared causal variant.
The signal-level summary was used because both loci could contain more than one association signal in at least one trait. A single top-SNP comparison would not distinguish one shared signal from multiple linked signals. For each locus, the final direction was assigned from the harmonised effects of variants shared by the selected signal credible sets, with the top shared variant reported as a descriptive anchor rather than as a proven causal variant.

### LAVA sensitivity and reproducibility

LAVA version 0.1.5 was used only for L006 and L007 with the Advanced AMD rescue and overall POAG summary statistics. The reference was 1000 Genomes Phase 3 EUR, and the fixed seed was 20260909. No explicit sample-overlap matrix was supplied. LAVA was interpreted as local-correlation sensitivity using the same summary statistics, not as independent replication.

Analyses were performed with R 4.4.x, Python 3.9.6, `susieR` 0.14.2, `coloc` 5.2.3, LAVA 0.1.5 and PLINK2 2.0.0-a.7.3 M1. Phase 4 outputs, scripts, command records, frozen configurations and checksums are retained in the project directory. The reproducibility repository is publicly available at https://github.com/seefreewind/amd-poag-antagonistic-pleiotropy and archived on Zenodo at https://doi.org/10.5281/zenodo.22689068.
The final artifacts include quantitative-LD QC JSON files, unified coloc tables, LAVA output, the final evidence table, figure source data and the deterministic figure-generation script. SHA256 hashes are recorded in the supplementary methods and in the final freeze. These records allow the manuscript values to be checked without rerunning the upstream discovery analyses.

## Results

### Dataset structure and global genetic relationship

The analytical dataset comprised the primary and rescue Advanced AMD resources, overall POAG, two statistically dependent POAG components, Early AMD and an NTG sensitivity resource. Their sample sizes, phenotype definitions, builds and analytical roles are summarised in Table 1. The primary conclusion was based on the European Advanced AMD–overall POAG pair; the component datasets were retained to describe the broader frozen phenotype matrix and were not treated as independent cohorts.

In the primary no-MHC LDSC analysis, Advanced AMD and POAG showed a negative genetic correlation (rg = −0.1798, SE = 0.0665, P = 0.0068; BH-FDR = 0.0113). The estimate used 1,172,447 HapMap3-filtered SNPs. The corresponding observed-scale SNP heritability estimates were 0.3405 (SE = 0.1171) for Advanced AMD and 0.0632 (SE = 0.0048) for POAG. The full phenotype-matrix context is shown in Fig. 1. The sign and uncertainty were compatible with a net opposing genome-wide relationship under the frozen LDSC model. This global estimate establishes a negative genome-wide relationship; it does not identify the loci or directions responsible for that relationship.
The primary estimate also provides the scale against which locus-level results should be read. Its magnitude is modest relative to the possible range of a correlation parameter, and its standard error remains material. The result is therefore useful as an architectural summary rather than as a direct count of antagonistic loci. The subsequent analyses were designed to test how much of the shared-locus evidence could be resolved beyond this aggregate parameter.

### Robustness and local-correlation context

The global estimate retained its direction in the full-effect Advanced AMD rescue analysis (rg = −0.164, SE = 0.067, P = 0.0143). Removing the major AMD regions also retained a negative estimate: rg = −0.1750 after APOE removal, rg = −0.1906 after ARMS2/HTRA1 removal and rg = −0.2316 after CFH removal. Leave-one-chromosome-out estimates ranged approximately from −0.2209 to −0.1659, with all chromosome-exclusion estimates remaining negative (Table 2). These results support direction robustness to the prespecified exclusions, without identifying a particular biological source. The CFH exclusion produced the most negative estimate among the reported major-locus sensitivities, whereas the APOE and ARMS2/HTRA1 exclusions remained close to the primary estimate in direction and scale.
The rescue LDSC was used to establish compatibility of the global direction with the full-effect resource needed for locus-level analyses. Because the rescue resource was related to the primary AMD programme, the concordant direction was treated as a resource-level sensitivity result rather than independent replication. The major-locus and LOCO analyses therefore strengthen the interpretation of a stable direction within the frozen dataset structure, while leaving external generalisability open.

HDL-L evaluated 2,463 predefined blocks, of which 696 produced finite estimates. No block reached BH-FDR < 0.05; the minimum finite BH-FDR was 0.3007 (Table 2 and Fig. 2). The negative local scan therefore did not provide a genome-wide catalogue of statistically supported regional correlations. This result was retained as an important boundary on the interpretation of L006 and as context for the subsequent restricted locus-level sensitivity analyses. The chromosome-exclusion profile is shown in Fig. 3.

### Discovery identifies heterogeneous shared-locus directions

The frozen cross-trait discovery stage identified 44 cFDR variants and 259 PLACO variants. Their intersection contained 41 variants grouped into seven locus windows. Five loci had opposite discovery direction and two were concordant. The seven-locus summary, including the frozen Phase 3.5 classifications and the Phase 4 fields for L006 and L007, is shown in Table 3. The final evidence categories were one candidate opposite-effect shared signal, four opposite-direction shared discovery loci without Phase 4 shared-signal adjudication, and two concordant shared loci. The discovery set was therefore directionally heterogeneous rather than uniformly antagonistic.
The discovery counts describe the output of two complementary prioritization procedures and should not be read as 41 shared causal variants. L001–L005 retained their frozen Phase 3.5 status because the final project scope did not authorize a new Phase 4 adjudication for those windows. L006 and L007 were the only loci carried through the quantitative-LD and unified multi-signal workflow. This created a defined evidence hierarchy rather than a reclassification of all seven loci.

### L006 shows a candidate opposite-effect shared signal

L006 was located in the expanded GRCh37 interval chr22:28,100,711–30,130,300. Quantitative EUR LD covered 737 of 738 requested variants (coverage 0.998645). The maximum cross-block absolute correlation was 0.5092, the maximum cross-block r² was 0.2593, and no cross-block pair reached r² ≥ 0.50. Both unified SuSiE fits converged using 721 aligned variants. The Advanced AMD fit contained one signal and a 24-variant credible set; the POAG fit contained three signals.

The unified coloc.susie analysis gave PP4 = 0.975590, and the signal-level credible sets overlapped at 10 variants. The top shared variant was rs1547014. After reference-allele harmonization, the Advanced AMD and POAG effects at rs1547014 were opposite. L006 therefore met the frozen technical rule for the candidate opposite-effect shared-signal category. The local sensitivity estimates are shown in Fig. 4, and the paired evidence display is shown in Fig. 5.
The quantitative-LD result also reduced the specific concern that cross-block correlation could make the original block-level signal uninterpretable. The maximum cross-block r² was below the prespecified 0.50 threshold, while the maximum absolute r remained 0.5092, so the cross-block structure was reported rather than treated as absent. The resulting designation reflects convergence of discovery, LD QC, multi-signal representation, shared-signal posterior support and harmonised direction, with the remaining uncertainty stated explicitly.

LAVA estimated a negative local correlation at L006 (rho = −0.331961, 95% CI −0.78294 to 0.05909, P = 0.0941787). The overlapping HDL-L chr22.12 block also had a negative estimate (rg = −0.8294, P = 0.07058; 95% likelihood interval −1.0000 to 0.0737). The direction was concordant across these two local summaries, but neither provided statistically definitive evidence after the broader analysis context. Both used the same underlying summary-statistics resources and were not independent replication.
The LAVA confidence interval included zero and the HDL-L likelihood interval extended to zero. These local estimates consequently function as directional context for L006, not as a second discovery criterion. Their inclusion makes the evidence chain transparent and prevents the PP4 result from being presented without its local-correlation uncertainty.

### L007 provides a concordant shared-signal contrast

L007 occupied chr22:32,605,227–33,611,247. The quantitative EUR reference contained 720 of 723 requested variants (coverage 0.995851), and the relevant direct-candidate proxy audit had r² = 1. Unified SuSiE fits converged using 705 aligned variants. The Advanced AMD fit contained three signals and the POAG fit contained one signal.

L007 also showed strong shared-signal support, with PP4 = 0.967815 and signal-level credible-set overlap of three variants. The top shared variant was rs5749498, but the harmonized effects were concordant. LAVA estimated rho = 0.0671874 (95% CI −0.22246 to 0.36139, P = 0.639564). The overlapping HDL-L chr22.16 estimate was weakly negative (rg = −0.1385, P = 0.7353; 95% likelihood interval −0.8100 to 0.6272). L007 was therefore classified as a concordant shared-signal contrast and was not counted as an antagonistic locus. The paired result is informative because the two loci were handled with the same reference panel, credible-set framework and posterior threshold. The difference in final category was driven by the harmonised direction of the shared variants, not by selectively applying a stronger method to L006.

### Genome-wide covariance and locus-level direction are non-equivalent

The final synthesis is presented in Fig. 6. First, the primary and rescue LDSC estimates were negative and retained their direction after major-locus and chromosome exclusion. Second, the HDL-L scan did not identify a BH-FDR-significant local block. Third, L006 provided the strongest locus-specific candidate after quantitative-LD and unified fine-mapping adjudication. Fourth, L007 showed that similarly strong shared-signal support can occur with concordant effects.

Removing L006 from the Advanced AMD rescue–POAG LDSC input changed the estimate from rg = −0.164 (SE = 0.067, P = 0.0143) to rg = −0.162 (SE = 0.0666, P = 0.0150), a change of 0.002 (Table 2). The negative genome-wide estimate was therefore not materially explained by L006 alone. The combined pattern is consistent with opposing architecture containing heterogeneous locus-level directions, while leaving the specific biological mechanism unresolved.
This removal result is a sensitivity statement about contribution to the genome-wide estimate, not a proof that the remaining correlation is diffuse or biologically homogeneous. The seven-locus pattern and the null HDL-L scan suggest that the global and local levels are not interchangeable. Together, the results support a layered interpretation: a negative genome-wide relationship, a focused candidate opposite-effect shared signal and a concordant shared-signal contrast.

## Discussion

Three conclusions define the study. First, Advanced AMD and POAG showed a negative genome-wide genetic relationship that persisted across the frozen rescue, major-locus and chromosome-exclusion analyses. Second, L006 met the prespecified candidate opposite-effect shared-signal category after quantitative EUR LD, multi-signal fine-mapping and coloc.susie adjudication. Third, L007 had similarly strong shared-signal support but concordant effects under the same workflow. The primary contribution was therefore the direction-resolved separation of global covariance, shared-signal evidence and allelic direction. The data support opposing genetic architecture with heterogeneous locus-level directions; they do not establish disease-wide confirmed antagonistic pleiotropy.
This framing changes the inferential endpoint of the paper. The outcome is not a binary decision that the two diseases either do or do not exhibit antagonistic pleiotropy. It is a structured assignment of evidence: genome-wide covariance at one level, local shared-signal support at another, and effect direction after harmonization. Such a structure allows a strong candidate to be reported while preserving the concordant locus and the negative local scan that constrain interpretation.

### Genome-wide covariance is not locus-level antagonistic pleiotropy

Genetic correlation is an aggregate parameter that summarises covariance across many variants. LDSC can produce a negative estimate when the genome contains a mixture of concordant and discordant loci, when small opposing effects are distributed across many regions, or when the magnitudes of shared effects are unequal. The value of rg does not show that every shared locus is opposite, and it does not establish that the same causal variant influences both traits. The unchanged direction after major-locus and chromosome exclusion supports the stability of the estimate within the frozen analyses, but it does not identify the mechanism of the covariance.

This distinction is particularly important for two diseases with different principal tissues and phenotype definitions. Advanced AMD includes geographic atrophy and/or choroidal neovascularization, whereas POAG combines clinically ascertained disease states and statistically derived components. Cross-trait covariance may therefore reflect distributed susceptibility, disease-stage composition, or correlated regional architecture. The current results narrow the interpretation to a negative genome-wide relationship and a directionally heterogeneous shared-locus set.

### L006 and L007 provide the central methodological contrast

L006 is the strongest locus-specific candidate in the frozen project. Its Phase 4 analysis addressed the earlier limitation of inadequate quantitative cross-block LD with an auditable 1000 Genomes EUR reference. Coverage was nearly complete, the matrix passed QC, both multi-signal SuSiE fits converged, PP4 was 0.975590 and 10 signal-level credible-set variants overlapped. The opposite direction at rs1547014 remained after harmonization. These results justify the candidate opposite-effect shared-signal designation.

The designation remains narrower than a causal or mechanistic claim. The reference panel contained 503 EUR samples, the summary-statistics inputs may have unknown participant overlap, the local LAVA estimate was not statistically definitive, and no independent replication cohort was available. A high PP4 is evidence for a shared-signal configuration under a specified model. It does not prove that one variant is causal or that the shared signal protects against one disease while increasing risk for the other.

L007 makes this boundary visible. It passed the same quantitative-LD and unified fine-mapping workflow and had PP4 = 0.967815 with three overlapping signal-level credible-set variants. Its harmonized direction was concordant, and its LAVA estimate was weakly positive. This is not a failed analysis; it is the internal contrast required to show that shared-signal support and opposite direction are separable properties. The contrast also prevents the global negative estimate from being interpreted as a requirement that all shared loci point in opposite directions.

### Relationship to previous genetic studies

The present analysis builds on large AMD and POAG GWAS resources rather than replacing them. The original Advanced AMD GWAS and subsequent early AMD analysis established complementary stage-specific resources (Fritsche et al. 2016; Winkler et al. 2020). Large POAG meta-analysis and GWAS-by-subtraction provided the overall and conditional glaucoma phenotypes used here (Gharahkhani et al. 2021; Huang et al. 2024). The rescue AMD resource extends the available effect-size information in an updated IAMDGC dataset (Gorski et al. 2025).

Earlier work reported positive or suggestive AMD–POAG genetic overlap using smaller datasets and different estimands (Cuellar-Partida et al. 2016). A recent integrative study reported a negative AMD–POAG genetic correlation in a broader analysis that also included cataract, Mendelian randomization and single-cell expression (Bai et al. 2026). The current study does not seek to adjudicate those additional causal or cellular analyses. It adds a narrower contribution: it makes the direction of shared signals an explicit inferential layer and demonstrates the distinction with the L006–L007 pair. Broader ocular pleiotropy studies provide context for cross-disease sharing, but they do not remove the need for locus-specific LD and direction checks (Yao et al. 2023).

### Complementary methods and their limits

The methods used here answer different questions. cFDR prioritizes variants under cross-trait enrichment, PLACO tests a composite null for pleiotropy, SuSiE represents multiple association signals, and coloc.susie evaluates posterior support for alternative signal configurations (Andreassen et al. 2013; Ray and Chatterjee 2020; Wang et al. 2020; Zou et al. 2022; Giambartolomei et al. 2014). LDSC, HDL-L and LAVA provide genome-wide or local-correlation context using different modelling frameworks (Bulik-Sullivan et al. 2015; Ning et al. 2020; Werme et al. 2022). Their convergence at L006 increases the structure of the statistical evidence, but their shared dependence on the same GWAS summary statistics means that they are not independent confirmations.

The quantitative LD step was important because binary LD availability was insufficient for the original L006 adjudication. The 1000 Genomes Phase 3 reference provides a transparent European LD basis (The 1000 Genomes Project Consortium 2015), but its sample size and ancestry composition limit fine-mapping resolution. Larger, ancestry-matched reference panels and individual-level conditional analyses would help distinguish a shared causal configuration from correlated association patterns and multiple linked signals.
The use of a quantitative signed LD matrix also clarifies why a locus-level result should not be reduced to physical proximity or a single lead SNP. At L006, the matrix permitted explicit assessment of cross-block correlations and a unified representation of multiple signals. At L007, it allowed the same workflow to be applied to a concordant contrast. This methodological symmetry is more informative than a list of loci ranked only by discovery P value.

### Strengths, limitations and future validation

Strengths include the staged freeze before final locus adjudication, retention of both primary and rescue global estimates, explicit direction harmonization, quantitative LD QC, multi-signal fine-mapping, the paired L006/L007 workflow and retention of negative HDL-L results. The manuscript also separates technical evidence categories from biological and clinical claims.

The main limitations are specific. No independent GWAS replication cohort was available for L006 or L007. The rescue AMD resource is related to the primary programme, and participant-level overlap between public AMD and POAG files could not be reconstructed. LAVA lacked an explicit sample-overlap matrix. The quantitative LD reference contained 503 EUR samples, and summary-statistics fine-mapping cannot prove a shared causal variant. HDL-L did not identify a BH-FDR-significant local block, which may reflect local power, reference structure or the distribution of effects. The POAG component datasets are statistically dependent decompositions. The European ancestry design limits generalisability, and phenotype definitions differ across sources. Finally, several methods use the same summary statistics, so apparent convergence does not remove shared-data dependence.
These limitations also affect the strength of any biological interpretation. The candidate direction is reference-oriented and depends on successful allele harmonization; the available phenotype definitions do not establish that the same disease stage was compared across resources; and the absence of a significant HDL-L block cannot distinguish lack of regional covariance from limited power. The study did not include individual-level conditional modelling or functional experiments. These constraints are why the manuscript uses “candidate opposite-effect shared signal” as its endpoint and reserves mechanistic language for future work.

The next step is independent replication of L006 in non-overlapping Advanced AMD and POAG datasets with harmonized phenotype definitions and documented sample overlap. Larger and ancestry-diverse LD references could test the stability of the shared-signal configuration. Individual-level conditional analyses could separate correlated association from multiple causal signals, and functional studies could evaluate hypotheses generated by the statistical evidence. None of these validation steps was performed here.

## Conclusions

AMD and POAG show a negative genome-wide genetic relationship with heterogeneous locus-level directions. L006 is a candidate opposite-effect shared signal supported by quantitative EUR LD, unified fine-mapping and coloc.susie, whereas L007 provides a concordant shared-signal contrast under the same workflow. The main contribution is the explicit separation of genome-wide covariance, shared-signal support and harmonized allelic direction. Independent genetic and functional validation is required before stronger mechanistic or translational conclusions are warranted.

## References

Andreassen, O. A. *et al.* Improved detection of common variants associated with schizophrenia and bipolar disorder using pleiotropy-informed conditional false discovery rate. *PLoS Genetics* **9**, e1003455 (2013). https://doi.org/10.1371/journal.pgen.1003455

Bai, Z.-P., Pan, Y.-S., Cai, Y.-X., Chen, C., Tao, D., Zhao, X.-Y., Shen, Y.-F., Chen, F., Li, J.-H., Qu, J. & Huang, X.-F. Investigating the shared genetic architecture of 3 age-related ocular disorders. *Ophthalmology Science* **6**, 100942 (2026; online 2025). https://doi.org/10.1016/j.xops.2025.100942

Bulik-Sullivan, B. K. *et al.* LD Score regression distinguishes confounding from polygenicity in genome-wide association studies. *Nature Genetics* **47**, 291–295 (2015). https://doi.org/10.1038/ng.3211

Cuellar-Partida, G. *et al.* Assessment of polygenic effects links primary open-angle glaucoma and age-related macular degeneration. *Scientific Reports* **6**, 26885 (2016). https://doi.org/10.1038/srep26885

Diaz-Torres, S. *et al.* Genome-wide meta-analysis identifies 22 loci for normal tension glaucoma with significant overlap with high tension glaucoma. *Nature Communications* **15**, 9959 (2024). https://doi.org/10.1038/s41467-024-54301-2

Fritsche, L. G. *et al.* A large genome-wide association study of age-related macular degeneration highlights contributions of rare and common variants. *Nature Genetics* **48**, 134–143 (2016). https://doi.org/10.1038/ng.3448

Gharahkhani, P. *et al.* Genome-wide meta-analysis identifies 127 open-angle glaucoma loci with consistent effect across ancestries. *Nature Communications* **12**, 1258 (2021). https://doi.org/10.1038/s41467-020-20851-4

Giambartolomei, C. *et al.* Bayesian test for colocalisation between pairs of genetic association studies using summary statistics. *PLoS Genetics* **10**, e1004383 (2014). https://doi.org/10.1371/journal.pgen.1004383

Gorski, M. *et al.* Diverse-ancestry GWAS of age-related macular degeneration on 16,108 examined cases and 18,038 controls. *Investigative Ophthalmology & Visual Science* **66**, 51 (2025). https://doi.org/10.1167/iovs.66.13.51

Huang, Y. *et al.* GWAS-by-subtraction reveals an IOP-independent component of primary open angle glaucoma. *Nature Communications* **15**, 8962 (2024). https://doi.org/10.1038/s41467-024-53331-0

Ning, Z., Pawitan, Y. & Shen, X. High-definition likelihood inference of genetic correlations across human complex traits. *Nature Genetics* **52**, 859–864 (2020). https://doi.org/10.1038/s41588-020-0653-y

Ray, D. & Chatterjee, N. A powerful method for pleiotropic analysis under composite null hypothesis identifies novel shared loci between type 2 diabetes and prostate cancer. *PLoS Genetics* **16**, e1009218 (2020). https://doi.org/10.1371/journal.pgen.1009218

The 1000 Genomes Project Consortium. A global reference for human genetic variation. *Nature* **526**, 68–74 (2015). https://doi.org/10.1038/nature15393

Wang, G., Sarkar, A., Carbonetto, P. & Stephens, M. A simple new approach to variable selection in regression, with application to genetic fine mapping. *Journal of the Royal Statistical Society: Series B* **82**, 1273–1300 (2020). https://doi.org/10.1111/rssb.12388

Werme, J., van der Sluis, S., Posthuma, D. & de Leeuw, C. A. An integrated framework for local genetic correlation analysis. *Nature Genetics* **54**, 274–282 (2022). https://doi.org/10.1038/s41588-022-01017-y

Winkler, T. W. *et al.* Genome-wide association meta-analysis for early age-related macular degeneration highlights novel loci and insights for advanced disease. *BMC Medical Genomics* **13**, 120 (2020). https://doi.org/10.1186/s12920-020-00760-7

Yao, X., Yang, H., Han, H. *et al.* Genome-wide analysis of genetic pleiotropy and causal genes across three age-related ocular disorders. *Human Genetics* **142**, 507–522 (2023). https://doi.org/10.1007/s00439-023-02542-4

Zou, Y., Carbonetto, P., Wang, G. & Stephens, M. Fine-mapping from summary data with the “Sum of Single Effects” model. *PLoS Genetics* **18**, e1010299 (2022). https://doi.org/10.1371/journal.pgen.1010299

## Statements and Declarations

### Acknowledgements

None.

### Funding

No funding was received for this study.

### Competing Interests

The authors declare no competing interests.

### Author Contributions

Da Lin: Conceptualization, Data curation, Formal analysis, Methodology, Software, Visualization, Writing – original draft. Ying Chen: Data curation, Investigation, Validation, Writing – review and editing. Yue Liu: Investigation, Validation, Visualization, Writing – review and editing. Yu Zhang: Conceptualization, Methodology, Supervision, Project administration, Resources, Writing – review and editing.

### Ethics approval and consent to participate

This study used publicly available GWAS summary statistics and an external public genotype reference. No new individual-level data were collected, and no new participant-level analysis was performed. The ethics approvals and consent procedures of the original contributing studies apply. The authors should confirm the exact source-study ethics wording before submission.

### Consent for publication

Not applicable. No individual-level identifiable data, participant images or individually identifiable information are included. [AUTHOR CONFIRMATION NEEDED]

### Data Availability

GWAS source metadata, sample-size information, access links and checksums are documented in `metadata/GWAS_MANIFEST.tsv`. Frozen Phase 4 quantitative-LD QC, unified fine-mapping outputs, LAVA outputs, figure source data and final evidence tables are retained under `results/phase4/` and `results/figures/`. Access to source summary statistics and reference data remains subject to the terms of the original data providers. The reproducibility repository is publicly available at https://github.com/seefreewind/amd-poag-antagonistic-pleiotropy and its archived release is available on Zenodo at https://doi.org/10.5281/zenodo.22689068.

### Code Availability

The analysis scripts, frozen configurations, compact derived results and figure-generation scripts are available in the public repository https://github.com/seefreewind/amd-poag-antagonistic-pleiotropy and its archived Zenodo release (https://doi.org/10.5281/zenodo.22689068).
