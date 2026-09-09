# Phase 4 当前状态

## 结论

Phase 4 已完成。L006 由 Phase 3.5 的 Tier 2 升级为 Phase 4 Tier 1 候选拮抗性位点；L007 的一次性定量 LD rescue 完成后被确认是 concordant shared-signal locus，不支持拮抗方向。全局结果仍是负向遗传相关，HDL-L 全局区块扫描没有通过 BH-FDR 的局部区块。

这支持论文进入“条件性写作”阶段，主张应限定为：**Advanced AMD–POAG 存在负向全局遗传架构，并在 L006 观察到一个具有统一共享信号和相反效应方向的候选拮抗性位点。** 结果尚不支持疾病层面的 confirmed antagonistic pleiotropy、独立复制或临床/治疗结论。

## L006 定量 LD 与统一精细定位

| 项目 | 结果 |
|---|---|
| EUR reference | 1000 Genomes Phase 3 EUR；503 samples；GRCh37 |
| quantitative LD | 737/738 requested variants；coverage 0.9986；PSD QC PASS |
| cross-block LD | max |r| = 0.5092；max r² = 0.2593；无 r²≥0.50 的 cross-block pair |
| unified SuSiE | AMD 721 SNP、1 signal、CS size 24；POAG 721 SNP、3 signals；两者均 converged |
| unified coloc.susie | PP4 = 0.975590；signal-level CS overlap = 10；status PASS |
| shared signal | rs1547014；reference-oriented effects remain opposite |
| LAVA | rho = −0.331961；95% CI −0.78294–0.05909；P = 0.0941787 |
| HDL-L overlap | chr22.12 rg = −0.8294，P = 0.07058；方向与 LAVA 一致但未通过局部多重校正 |
| final phase | TIER1 candidate antagonistic locus |

LAVA 和 HDL-L 的局部 P 值只作定向敏感性证据，不替代全局多重校正，也不构成独立复制。

## L007 定量 rescue 与统一精细定位

| 项目 | 结果 |
|---|---|
| direct candidate coverage | rs5749498、rs756481、rs12170368 均直接存在；r²=1 |
| quantitative LD | 720/723 requested variants；coverage 0.9959；PSD QC PASS |
| unified SuSiE | AMD 705 SNP、3 signals；POAG 705 SNP、1 signal；两者均 converged |
| unified coloc.susie | PP4 = 0.967815；signal-level CS overlap = 3；status PASS |
| shared signal | rs5749498；reference-oriented effects concordant |
| LAVA | rho = 0.0671874；95% CI −0.22246–0.36139；P = 0.639564 |
| HDL-L overlap | chr22.16 rg = −0.1385，P = 0.7353；局部估计弱且方向不一致 |
| final phase | CONCORDANT；不计入拮抗性位点 |

## Final tier counts

Phase 4 final table: TIER1 = 1（L006）、TIER3 = 4（L001–L004）、CONCORDANT = 2（L005、L007）。Phase 3.5 原始 tier table 保留不变；Phase 4 新表为 `results/phase4/FINAL_ANTAGONISTIC_TIER_TABLE_PHASE4.tsv`。

## 审计边界

- 未重跑 Phase 0–3.5、genome-wide cFDR、PLACO 或 discovery fine-mapping。
- 未进入单细胞、多组学、eQTL、TWAS、MR、药物靶点或通路扩展。
- LAVA 仅分析 Advanced AMD rescue × overall POAG 的 L006/L007；没有分析 POAG IOP/non-IOP 组件。
- LAVA 使用同一组 summary statistics 和 1000G EUR reference；sample-overlap file 未提供，因此按无显式样本重叠矩阵运行。该结果是方法学敏感性分析，不是独立复制。
- 任何“shared causal variant”表述都应改写为“shared-signal configuration”或“candidate shared signal”，因为 summary-statistics fine-mapping 不能单独证明因果变异。
