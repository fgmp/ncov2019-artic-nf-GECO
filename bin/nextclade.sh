#!/usr/bin/env bash

fasta_path=$1

nextclade \
   --in-order \
   --input-fasta ${fasta_path}\
   --input-dataset ~/envs/nextclade_test/data/sars-cov-2 \
   --output-tsv nextclade.tsv