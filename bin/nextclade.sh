#!/usr/bin/env bash

# installs latest nextclade build and says yes to prompts

fasta_path=$1
baseDir=$2
nextclade dataset get --name 'sars-cov-2' --output-dir "${baseDir}/data/sars-cov-2"

nextclade run \
   -D "${baseDir}/data/sars-cov-2" \
   --output-tsv=nextclade.tsv \
   ${fasta_path}
