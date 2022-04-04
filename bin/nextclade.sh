#!/usr/bin/env bash

fasta_path=$1


nextclade --version

nextclade dataset get --name 'sars-cov-2' --output-dir '/data/apps/ncov2019-artic-nf_automated/data/sars-cov-2'

nextclade \
   --in-order \
   --input-fasta ${fasta_path}\
   --input-dataset /data/apps/ncov2019-artic-nf_automated/data/sars-cov-2 \
   --output-tsv nextclade.tsv
