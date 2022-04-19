#!/usr/bin/env bash

# installs latest nextclade build and says yes to prompts

fasta_path=$1
baseDir=$2
nextclade dataset get --name 'sars-cov-2' --output-dir "${baseDir}/data/sars-cov-2"

nextclade \
   --in-order \
   --input-fasta ${fasta_path}\
   --input-dataset "${baseDir}/data/sars-cov-2" \
   --output-tsv nextclade.tsv
