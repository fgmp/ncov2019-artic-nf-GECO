#!/usr/bin/env python3

import sys

import pandas as pd
from pyfaidx import Fasta

# Prepare dictionary for swapping headers.
collated_db = pd.read_csv(sys.argv[1], sep=",", index_col=None)
df_header_swap = collated_db[
    ["fasta", "gisaid_name"]].set_index("fasta")
header_swap = df_header_swap.to_dict()
header_swap = header_swap["gisaid_name"]

# Swap old to new headers.
single_fasta = sys.argv[2]
sequence_header_swapped = Fasta(
    single_fasta, sequence_always_upper=True,
    read_long_names=False,
    key_function=lambda x:
      header_swap[single_fasta] if single_fasta in header_swap else x
    )

# Write new single_fasta to file.
new_single_fasta = []
for record in sequence_header_swapped:
    edited_name = ">"+record.name+"\n"
    orig_seq = str(record)+"\n"
    new_single_fasta.append(edited_name)
    new_single_fasta.append(orig_seq)
    new_single_fasta = "".join(new_single_fasta)
    new_single_fasta_name = record.name+".fasta"
    with open(new_single_fasta_name, "w") as out:
        out.write(new_single_fasta)

