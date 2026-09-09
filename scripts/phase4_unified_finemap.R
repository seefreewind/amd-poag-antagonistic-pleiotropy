#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
  library(jsonlite)
  library(susieR)
  library(coloc)
})

args <- commandArgs(trailingOnly = TRUE)
project <- normalizePath(if (length(args)) args[[1]] else ".", mustWork = TRUE)
phase4 <- file.path(project, "results/phase4")
dir.create(file.path(phase4, "L006_unified_susie"), recursive = TRUE, showWarnings = FALSE)

comp <- function(x) chartr("ACGT", "TGCA", x)

align_to_ref <- function(d, trait) {
  a1 <- d[[paste0("A1_", trait)]]
  a2 <- d[[paste0("A2_", trait)]]
  rel <- rep("mismatch", nrow(d))
  rel[a1 == d$LD_A1 & a2 == d$LD_A2] <- "exact"
  rel[rel == "mismatch" & a1 == d$LD_A2 & a2 == d$LD_A1] <- "swapped"
  rel[rel == "mismatch" & comp(a1) == d$LD_A1 & comp(a2) == d$LD_A2] <- "complement"
  rel[rel == "mismatch" & comp(a1) == d$LD_A2 & comp(a2) == d$LD_A1] <- "complement_swapped"
  mult <- ifelse(rel %in% c("swapped", "complement_swapped"), -1, 1)
  d[[paste0("relation_", trait)]] <- rel
  d[[paste0("beta_ref_", trait)]] <- d[[paste0("BETA_", trait)]] * mult
  d[[paste0("z_ref_", trait)]] <- d[[paste0("Z_", trait)]] * mult
  d[[paste0("varbeta_ref_", trait)]] <- d[[paste0("SE_", trait)]]^2
  d
}

make_sumstats <- function(path, trait, start, end) {
  z <- fread(path, select = c("SNP", "CHR", "BP", "A1", "A2", "BETA", "SE", "Z", "N"),
             na.strings = c("", "NA"), showProgress = FALSE)
  z <- z[CHR == 22 & BP >= start & BP <= end]
  setnames(z, c("SNP", "A1", "A2", "BETA", "SE", "Z", "N"),
           c("variant", paste0("A1_", trait), paste0("A2_", trait), paste0("BETA_", trait),
             paste0("SE_", trait), paste0("Z_", trait), paste0("N_", trait)))
  z
}

fit_one <- function(d, trait) {
  coloc::runsusie(
    d, suffix = trait, maxit = 100, repeat_until_convergence = FALSE, L = 10,
    coverage = 0.95, estimate_residual_variance = FALSE, prior_variance = 50,
    check_prior = TRUE, max_iter = 100, tol = 0.001
  )
}

cs_list <- function(s) {
  if (is.null(s$sets) || is.null(s$sets$cs) || !length(s$sets$cs)) return(list())
  lapply(s$sets$cs, as.integer)
}

cs_for_signal <- function(s, signal_index) {
  if (is.null(s$sets) || is.null(s$sets$cs) || !length(s$sets$cs)) return(integer())
  ids <- s$sets$cs_index
  if (is.null(ids)) ids <- seq_along(s$sets$cs)
  hit <- which(as.integer(ids) == as.integer(signal_index))
  if (!length(hit)) return(integer())
  as.integer(s$sets$cs[[hit[1]]])
}

cs_string <- function(s, snps) {
  cs <- cs_list(s)
  if (!length(cs)) return("")
  paste(vapply(seq_along(cs), function(i) paste0("L", i, ":", paste(snps[cs[[i]]], collapse = ",")), character(1)), collapse = ";")
}

cs_overlap <- function(s1, s2) {
  a <- cs_list(s1); b <- cs_list(s2)
  if (!length(a) || !length(b)) return(0L)
  max(vapply(a, function(x) max(vapply(b, function(y) length(intersect(x, y)), integer(1))), integer(1)))
}

posterior_row <- function(cs) {
  if (is.null(cs$summary) || !nrow(cs$summary)) return(NULL)
  p <- cs$summary
  p[which.max(p$PP.H4.abf), , drop = FALSE]
}

get_num <- function(row, name) if (is.null(row) || !(name %in% names(row))) NA_real_ else as.numeric(row[[name]][1])

write_susie_summary <- function(trait, s, snps) {
  cs <- cs_list(s)
  pip <- s$pip
  top <- if (length(pip)) which.max(pip) else NA_integer_
  purity <- NA_real_
  if (!is.null(s$sets$purity) && length(s$sets$purity)) purity <- min(s$sets$purity[, "min_abs_corr"], na.rm = TRUE)
  data.table(
    trait = trait, n_snps = length(snps), n_signals = length(cs),
    CS = cs_string(s, snps), CS_size = if (length(cs)) paste(vapply(cs, length, integer(1)), collapse = ";") else "",
    coverage = 0.95, purity = purity,
    top_SNP = if (is.na(top)) "" else snps[top], top_PIP = if (is.na(top)) NA_real_ else pip[top],
    convergence = isTRUE(s$converged), status = if (isTRUE(s$converged)) "PASS" else "NONCONVERGED"
  )
}

start <- 28100711L
end <- 30130300L
ld <- fread(file.path(phase4, "L006_QUANT_LD_MATRIX.tsv.gz"), showProgress = FALSE)
snps <- as.character(ld[[1]])
R <- as.matrix(ld[, -1, with = FALSE])
storage.mode(R) <- "double"
rownames(R) <- colnames(R) <- snps

h <- fread(file.path(phase4, "L006_QUANT_LD_HARMONIZATION.tsv"), na.strings = c("", "NA"), showProgress = FALSE)
amd <- make_sumstats(file.path(project, "data/processed/phase2_5/ADV_AMD_RESCUE_GRCh37.hm3_noMHC.tsv.gz"), "AMD", start, end)
poag <- make_sumstats(file.path(project, "data/processed/standardized/POAG.hm3_noMHC.tsv.gz"), "POAG", start, end)
d <- merge(h[, .(variant, LD_A1, LD_A2, included)], amd, by = "variant", all.x = TRUE)
d <- merge(d, poag, by = "variant", all.x = TRUE)
d <- d[variant %in% snps & included == TRUE]
d <- align_to_ref(d, "AMD")
d <- align_to_ref(d, "POAG")
common <- d[is.finite(BETA_AMD) & is.finite(SE_AMD) & SE_AMD > 0 & is.finite(Z_AMD) & is.finite(N_AMD) & N_AMD > 0 &
             is.finite(BETA_POAG) & is.finite(SE_POAG) & SE_POAG > 0 & is.finite(Z_POAG) & is.finite(N_POAG) & N_POAG > 0 &
             relation_AMD != "mismatch" & relation_POAG != "mismatch"]
common <- common[match(snps, variant)]
common <- common[!is.na(variant)]
if (nrow(common) < 50) stop("L006 common aligned SNP count is <50")
idx <- match(common$variant, snps)
Rk <- R[idx, idx, drop = FALSE]
min_eig <- min(eigen(Rk, symmetric = TRUE, only.values = TRUE)$values)
if (!is.finite(min_eig) || min_eig < -1e-6) stop("L006 quantitative LD matrix failed PSD check: ", min_eig)

d1 <- list(beta = common$beta_ref_AMD, varbeta = common$varbeta_ref_AMD, z = common$z_ref_AMD,
           snp = common$variant, N = median(common$N_AMD), type = "cc", LD = Rk)
d2 <- list(beta = common$beta_ref_POAG, varbeta = common$varbeta_ref_POAG, z = common$z_ref_POAG,
           snp = common$variant, N = median(common$N_POAG), type = "cc", LD = Rk)
s1 <- fit_one(d1, "AMD")
s2 <- fit_one(d2, "POAG")
s1$sets <- susie_get_cs(s1, coverage = 0.95, min_abs_corr = 0.5)
s2$sets <- susie_get_cs(s2, coverage = 0.95, min_abs_corr = 0.5)
s1$sets$cs_index <- as.integer(sub("^L", "", names(s1$sets$cs)))
s2$sets$cs_index <- as.integer(sub("^L", "", names(s2$sets$cs)))
saveRDS(list(AMD = s1, POAG = s2, snp = common$variant, LD = Rk, dataset1 = d1, dataset2 = d2),
        file.path(phase4, "L006_unified_susie", "L006_unified_susie_coloc_input.rds"))

susie_rows <- list(write_susie_summary("AMD", s1, common$variant), write_susie_summary("POAG", s2, common$variant))
fwrite(rbindlist(susie_rows), file.path(phase4, "L006_UNIFIED_SUSIE_SUMMARY.tsv"), sep = "\t", na = "NA")

status <- if (isTRUE(s1$converged) && isTRUE(s2$converged)) "PASS" else "NONCONVERGED"
coloc_row <- data.table(
  AMD_signal = "", POAG_signal = "", PP0 = NA_real_, PP1 = NA_real_, PP2 = NA_real_, PP3 = NA_real_, PP4 = NA_real_,
  AMD_CS = cs_string(s1, common$variant), POAG_CS = cs_string(s2, common$variant), CS_overlap_n = cs_overlap(s1, s2),
  signal_CS_overlap_n = NA_integer_, max_CS_pair_r2 = NA_real_, signal_CS_pair_r2 = NA_real_,
  top_shared_variant = "", direction = "", status = status
)
if (status == "PASS") {
  cs <- coloc::coloc.susie(s1, s2, p1 = 1e-4, p2 = 1e-4, p12 = 1e-5)
  saveRDS(cs, file.path(phase4, "L006_unified_susie", "L006_unified_coloc_susie.rds"))
  pr <- posterior_row(cs)
  if (!is.null(pr)) {
    coloc_row$AMD_signal <- as.character(pr$hit1)
    coloc_row$POAG_signal <- as.character(pr$hit2)
    coloc_row$PP0 <- get_num(pr, "PP.H0.abf")
    coloc_row$PP1 <- get_num(pr, "PP.H1.abf")
    coloc_row$PP2 <- get_num(pr, "PP.H2.abf")
    coloc_row$PP3 <- get_num(pr, "PP.H3.abf")
    coloc_row$PP4 <- get_num(pr, "PP.H4.abf")
  }
  a <- cs_list(s1); b <- cs_list(s2)
  if (length(a) && length(b)) {
    pairs <- as.data.table(expand.grid(i = seq_along(a), j = seq_along(b)))
    pairs[, overlap := mapply(function(i, j) intersect(a[[i]], b[[j]]), i, j, SIMPLIFY = FALSE)]
    pairs[, overlap_n := lengths(overlap)]
    pairs[, max_r2 := mapply(function(i, j) max(Rk[a[[i]], b[[j]], drop = FALSE]^2), i, j)]
    best <- pairs[order(-overlap_n, -max_r2)][1]
    coloc_row$max_CS_pair_r2 <- best$max_r2
    if (!is.null(pr) && all(c("idx1", "idx2") %in% names(pr))) {
      signal_a <- cs_for_signal(s1, pr$idx1[1])
      signal_b <- cs_for_signal(s2, pr$idx2[1])
      signal_shared <- intersect(signal_a, signal_b)
      coloc_row$signal_CS_overlap_n <- length(signal_shared)
      coloc_row$signal_CS_pair_r2 <- if (length(signal_a) && length(signal_b)) max(Rk[signal_a, signal_b, drop = FALSE]^2) else NA_real_
    } else {
      signal_shared <- integer()
    }
    if (length(signal_shared)) {
      shared <- signal_shared
      score <- common$beta_ref_AMD[shared] * common$beta_ref_POAG[shared]
      top <- shared[which.max(abs(score))]
      coloc_row$top_shared_variant <- common$variant[top]
      coloc_row$direction <- ifelse(score[which.max(abs(score))] < 0, "OPPOSITE", "CONCORDANT")
    }
  }
} else {
  coloc_row$status <- "NOT_RUN_NONCONVERGED"
}
fwrite(coloc_row, file.path(phase4, "L006_UNIFIED_COLOC.tsv"), sep = "\t", na = "NA")
write_json(list(
  status = coloc_row$status, n_common = nrow(common), min_eigenvalue = min_eig,
  AMD_converged = isTRUE(s1$converged), POAG_converged = isTRUE(s2$converged),
  frozen_parameters = list(L = 10, coverage = 0.95, prior_variance = 50, max_iter = 100, tol = 0.001,
                           estimate_residual_variance = FALSE, p1 = 1e-4, p2 = 1e-4, p12 = 1e-5),
  reference = "1000G_Phase3_EUR_GRCh37",
  note = "Unified L006 analyses use the quantitative EUR matrix after Phase 4 QC PASS; no Phase 0-3.5 discovery rerun was performed."
), file.path(phase4, "L006_UNIFIED_ANALYSIS_STATUS.json"), auto_unbox = TRUE, pretty = TRUE)
cat("phase4_unified_finemap_complete\n")
