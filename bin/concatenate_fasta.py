#!/home/tohoku/apps/miniconda3/envs/nextflow_conda_sandbox/bin/python
import os
import sys

#accepts fasta path from user
fasta_path = sys.argv[1]

#concatenates fasta files > single fasta
os.system("mkdir " + fasta_path + '/collate_sequences')
os.system("cat " + fasta_path + "/*.fasta > " + fasta_path + "/collate_sequences/all_sequences_test.fasta")

