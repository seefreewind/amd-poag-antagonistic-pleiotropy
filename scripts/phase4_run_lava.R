#!/usr/bin/env Rscript

lib <- Sys.getenv("LAVA_R_LIB", unset = "")
if (nzchar(lib) && dir.exists(lib)) .libPaths(c(lib, .libPaths()))
suppressPackageStartupMessages(library(LAVA))
suppressPackageStartupMessages(library(data.table))
suppressPackageStartupMessages(library(jsonlite))

args <- commandArgs(trailingOnly = TRUE)
project <- normalizePath(if (length(args)) args[[1]] else ".", mustWork = TRUE)
phase4 <- file.path(project, "results/phase4")
lava_dir <- file.path(phase4, "lava_inputs")
out_dir <- file.path(phase4, "lava")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
set.seed(20260909)

info_file <- file.path(lava_dir, "PHASE4_LAVA_INPUT.info")
loci <- read.loci(file.path(lava_dir, "PHASE4_LAVA_LOCI.txt"))
sumstats <- file.path(project, "data/processed/phase2_5/ADV_AMD_RESCUE_GRCh37.hm3_noMHC.tsv.gz")
poag <- file.path(project, "data/processed/standardized/POAG.hm3_noMHC.tsv.gz")

run_one <- function(id, prefix) {
  message("LAVA processing ", id)
  input <- process.input(info_file, sample.overlap.file = NULL, ref.prefix = prefix, phenos = c("AMD", "POAG"), input.dir = project)
  loc_row <- loci[loci$LOC == id, , drop = FALSE]
  if (nrow(loc_row) != 1) stop("Expected exactly one locus row for ", id)
  loc <- process.locus(loc_row, input, phenos = c("AMD", "POAG"), min.K = 2, prune.thresh = 99,
                       max.prop.K = 0.75, drop.failed = TRUE, max.block.size = 3000, cap.estimates = TRUE)
  if (is.null(loc)) stop("LAVA process.locus returned NULL for ", id)
  univ <- run.univ(loc, phenos = c("AMD", "POAG"), var = TRUE)
  bivar <- run.bivar(loc, phenos = c("AMD", "POAG"), target = "POAG", adap.thresh = c(1e-4, 1e-6),
                     p.values = TRUE, CIs = TRUE, param.lim = 1.25, cap.estimates = TRUE)
  saveRDS(list(input = input, locus = loc, univariate = univ, bivariate = bivar),
          file.path(out_dir, paste0(id, "_LAVA.rds")))
  univ <- as.data.table(univ)
  bivar <- as.data.table(bivar)
  univ[, locus := id]
  bivar[, locus := id]
  list(univ = univ, bivar = bivar, n_snps = loc$n.snps, K = loc$K,
       phenos = loc$phenos, h2_obs = loc$h2.obs, omega_cor = loc$omega.cor)
}

results <- list()
results[["L006"]] <- run_one("L006", file.path(lava_dir, "L006_1000G_EUR_RSID"))
results[["L007"]] <- run_one("L007", file.path(lava_dir, "L007_1000G_EUR_RSID"))

fwrite(rbindlist(lapply(results, `[[`, "univ"), fill = TRUE), file.path(out_dir, "LAVA_UNIVARIATE.tsv"), sep = "\t", na = "NA")
fwrite(rbindlist(lapply(results, `[[`, "bivar"), fill = TRUE), file.path(out_dir, "LAVA_BIVARIATE.tsv"), sep = "\t", na = "NA")
status <- list(
  status = "PASS",
  package = "LAVA",
  package_version = as.character(packageVersion("LAVA")),
  random_seed = 20260909,
  source = "https://github.com/josefin-werme/LAVA",
  reference = "1000G_Phase3_EUR",
  build = "GRCh37",
  n_reference_samples = 503,
  phenotypes = c("Advanced AMD rescue", "overall POAG"),
  sample_overlap_file = "NOT_PROVIDED",
  loci = lapply(results, function(x) list(n_snps = x$n_snps, K = x$K, phenotypes = x$phenos,
                                           h2_obs = x$h2_obs, omega_cor = x$omega_cor)),
  note = "LAVA was restricted to Advanced AMD x overall POAG at L006 and L007. No POAG components or other phenotype pairs were analysed."
)
write_json(status, file.path(out_dir, "LAVA_STATUS.json"), auto_unbox = TRUE, pretty = TRUE)
cat("phase4_lava_complete\n")
