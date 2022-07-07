#!/usr/bin/env python3
import sys
import re

import pandas as pd
import subprocess as sp

# Set thresholds.
mix_thresh = 0.8
depth_thresh = 20
pos_thresh = 4

# Read input anlyasis csv, set path to artic analysis folder.
#meta_folder = sys.argv[1]
nextclade_tsv = sys.argv[1]
analysis_folder = sys.argv[2]
#meta_analysis_csv = pd.read_csv(f'{meta_folder}/nextclade.tsv', sep='\t')
meta_analysis_csv = pd.read_csv(nextclade_tsv, sep='\t')

# Get mutations & N's from 15th & 16th element of each split.
#nextclade_snps = meta_analysis_csv.str[15]  # mutations
#nextclade_Ns = meta_analysis_csv.str[29]  # N's
nextclade_snps = meta_analysis_csv["substitutions"]  # mutations
nextclade_Ns = meta_analysis_csv["missing"]  # N's

# Drop NaN rows.
nextclade_snps.dropna(inplace=True)
nextclade_Ns.dropna(inplace=True)
print(nextclade_snps)
print(nextclade_Ns)


# Split nextclade_snps by ',' and remove letters from each element.
nextclade_snps = nextclade_snps.str.split(',').apply(
    lambda x: [re.sub('[A-Z]','',i) for i in x]
    )

# Split nextclade_Ns by ',' and isolate N's from single positions.
nextclade_Ns = nextclade_Ns.str.split(',').apply(
    lambda x: [i for i in x if "-" not in i]
    )


# Append all mutations and single N's to a list,
# exclude nan's and empty strings, and sort.
all_snps = []
all_single_Ns = []
all_snps_and_single_Ns = []
nextclade_snps = nextclade_snps.apply(lambda x: all_snps.extend(x))
nextclade_Ns = nextclade_Ns.apply(lambda x: all_single_Ns.extend(x))
all_snps = list(set(all_snps))
all_single_Ns = list(set(all_single_Ns))
print(all_snps)
print(all_single_Ns)
all_snps_and_single_Ns.extend(all_snps)
all_snps_and_single_Ns.extend(all_single_Ns)
all_snps_and_single_Ns = [
    i for i in all_snps_and_single_Ns if i != '' and i != 'nan'
    ]
all_snps_and_single_Ns = [int(i) for i in all_snps_and_single_Ns]
all_snps_and_single_Ns = list(set(all_snps_and_single_Ns))
all_snps_and_single_Ns.sort()
all_snps_and_single_Ns = [str(i) for i in all_snps_and_single_Ns]
all_snps_and_single_Ns = ' '.join(all_snps_and_single_Ns)


# Glob for names of all bam files in analysis folder.
bam_files = sp.check_output(
    f'find {analysis_folder} -name "*primertrimmed.rg.sorted.bam"', shell=True
    ).decode('utf-8').split('\n')
bam_files = [b for b in bam_files if b != '']

# Call bammix command from shell with all_snps_and_single_Ns as input.
# Use run name, barcode, and central_id as prefix.
for bam in bam_files:
    prefix  = re.sub('.primertrimmed.rg.sorted.bam','',bam.split('/')[1])
    bammix_cmd = f'bammix -b {bam} -p {all_snps_and_single_Ns} -o {prefix}'
    bammix_output = sp.check_output(bammix_cmd, shell=True).decode()
    # TO DO: Split list of positions if >N and cannot fit in one plot.

# Glob for names of all bammix csv files.
bammix_csv_files = sp.check_output(
    f'find ./ -name "*_position_base_counts.csv"', shell=True
    ).decode('utf-8').split('\n')
bammix_csv_files = [i for i in bammix_csv_files if i != '']

# Read all bammix csv files as df's.
bammix_csv = [pd.read_csv(f) for f in bammix_csv_files]


# Iterate over bammix df's, keep track which barcodes had bad mixtures,
# (i.e. >4 positions with >20% mixture at >20x depth),
# at what positions, and what bases.
bad_mixtures = []
bad_mixtures_positions = []
bad_mixtures_base_prop = []
for nam, df in zip(bammix_csv_files, bammix_csv):
    # Get barcode from file name.
    name = re.sub('_position_base_counts.csv','',nam)
    # Get df of nucleotide positions.
    df_pos = df[["Position"]]
    # Get positions with >20% mixture from df.
    df_prop = df[["A_proportion", "C_proportion", "G_proportion", "T_proportion"]]
    # Get largest number for each row in df.
    df_prop_max = df_prop.max(axis=1)
    # Select rows with less than 0.80 value in df_prop_max.
    df_prop_max_bool = df_prop_max < mix_thresh
    df_prop_below80max = df_prop[df_prop_max_bool]
    # Flag only if depth is >20 reads.
    df_depth = df[["Total_reads"]]
    df_depth_20x = df_depth["Total_reads"] > depth_thresh
    df_prop_below80max_20xdepth = df_prop_below80max[df_depth_20x]
    if df_prop_below80max_20xdepth.empty:
        pass
    elif df_prop_below80max_20xdepth.shape[0] > pos_thresh:
        bad_mixtures.append(name)
        bad_mixtures_positions.append(df_pos.iloc[df_prop_below80max_20xdepth.index].Position.tolist())
        bad_mixtures_base_prop.append(df_prop_below80max_20xdepth.values.tolist())

# Write table of flagged barcodes, positions, base proportions.
bammix_bad_mixtures_csv = pd.DataFrame()
bammix_bad_mixtures_csv['barcode'] = bad_mixtures
bammix_bad_mixtures_csv['positions'] = bad_mixtures_positions
bammix_bad_mixtures_csv['base_prop'] = bad_mixtures_base_prop
bammix_bad_mixtures_csv.to_csv("flagged_barcodes_positions_proportions.csv", index=False)

# Concatenate all raw bammix csv files into one csv for reference.
bammix_csv_pos_col = bammix_csv[0]["Position"]
for i in range(len(bammix_csv)):
    bammix_csv[i].columns = [
        f'{bammix_csv_files[i].split("/")[1]}_{c}'
        for c in bammix_csv[i].columns
        ]

bammix_csv = pd.concat(bammix_csv, ignore_index=False, axis=1)
position_cols = [c for c in bammix_csv.columns if 'Position' in c]
bammix_csv.drop(position_cols, axis=1, inplace=True)
bammix_csv = pd.concat([bammix_csv_pos_col,bammix_csv], ignore_index=False, axis=1)
bammix_csv.sort_values("Position", ascending=True, inplace=True, na_position='last')
bammix_csv.to_csv("concat_raw_bammix.csv", index=False)


