#!/usr/bin/Rscript --vanilla
#SBATCH -J {v}
#SBATCH -e {prefix}logs/{v_slug}.err
#SBATCH -o {prefix}logs/{v_slug}.out
#SBATCH --cpus-per-task=1
#SBATCH --mem=4096
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4096
#SBATCH --nodes=1

library(readr)
library(cegwas)
library(dplyr)

file_prefix <- "{prefix}"
input_data <- paste0(file_prefix, "phenotypes/", "{v_slug}", ".tsv")
output_tsv <- paste0(file_prefix, "mappings_tsv/", "{v_slug}", ".tsv")
output_rdata <- paste0(file_prefix, "mappings_rdata/", "{v_slug}", ".rdata")

df <- readr::read_tsv("{file_path}")


pheno <- process_pheno(df)
mapping_df <- gwas_mappings(pheno,  cores = 1, mapping_snp_set = F)
p_mapping_df <- process_mappings(mapping_df, phenotype_df = pheno, CI_size = 50, snp_grouping = 200)

readr::write_tsv(p_mapping_df, path = output_tsv)
save(p_mapping_df, file = output_rdata)


