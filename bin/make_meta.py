#!/usr/bin/env python3

import json
import sys
import xml.dom.minidom

import pandas as pd
from pyfaidx import Fasta 
import redcap
import requests

setting = sys.argv[1]
summaryfile = sys.argv[2]
metafile = sys.argv[3]
dag = sys.argv[4]
instance = sys.argv[5]
outfile = sys.argv[6] + ".redcap_meta.csv"

# Set key name for the metafile data to be collected.
meta_dict = {
    "central_id" : "",
    "gisaid_name" : "",
    "redcap_repeat_instance" : "",
    "redcap_data_access_group" : "",
    "local_id" : "",
    "rapid_local_id" : "",
    "diagnostic_local_id" : "",
    "sequence_local_id" : "",
    "project_id" : "",
    "flowcell_id" : "",
    "flowcell_type" : "",
    "instrument_make" : "",
    "instrument_model" : "",
    "run_name" : "",
    "library_strategy" : "",
    "analysis_local_id" : "",
}

# Set how summaryfile cols are renamed.
summary_rename_col = {
    "pct_covered_bases" : "missing",
    "ave_cov_depth" : "ave_depth",
}

# Set which summaryfile cols are dropped.
summary_drop_col = [
    "pct_N_bases",
    "longest_no_N_run",
    "num_aligned_reads",
    "fasta",
    "bam",
    "qc_pass",
]

# Read summaryfile as pandas dataframe.
summary_df = pd.read_csv(summaryfile, sep=",", header=0, index_col=0)

# Drop summaryfile columns in summary_drop_col.
summary_df = summary_df.drop(summary_drop_col, axis=1)

# Collect metadata for illumina.
if setting == "illumina":
    # Parse xml metafile.
    doc = xml.dom.minidom.parse(metafile)

    # Collect metafile RunID for run_name.
    meta_dict["run_name"] = str(doc.getElementsByTagName("RunID")[0].firstChild.nodeValue)
    
    # Collect metafile ExperimentName for project_id.
    meta_dict["project_id"] = str(doc.getElementsByTagName("ExperimentName")[0].firstChild.nodeValue)

    # Collect metafile FlowcellRFIDTag SerialNumber for flowcell_id.
    flowcell_childnodes = doc.getElementsByTagName("FlowcellRFIDTag")[0].childNodes
    for node in flowcell_childnodes:
        if str(node.nodeName) == "SerialNumber":
            meta_dict["flowcell_id"] = str(node.firstChild.nodeValue)
        # Collect metafile FlowcellRFIDTag PartNumber for flowcell_type.
        elif str(node.nodeName) == "PartNumber":
            meta_dict["flowcell_type"] = str(node.firstChild.nodeValue)

    # Collect metafile RunParametersVersion for instrument_make and instrument_model.
    runparamver_node = str(doc.getElementsByTagName("RunParametersVersion")[0].firstChild.nodeValue)
    if "MiSeq" in runparamver_node:
        meta_dict["instrument_make"] = 0
        meta_dict["instrument_model"] = 3
    else:
        raise ValueError("Instrument make/model not recognized from RunParametersVersion xml node.")

    # Collect metafile Chemistry for library_strategy.
    chemistry_node = str(doc.getElementsByTagName("Chemistry")[0].firstChild.nodeValue)
    if "Amplicon" in chemistry_node:
        meta_dict["library_strategy"] = 0
    else:
        raise ValueError("Library strategy not recognized from Chemistry xml node.")

    # Set redcap_data_access_group value to dag.
    meta_dict["redcap_data_access_group"] = dag

    # Set redcap_repeat_instance value to 1.
    meta_dict["redcap_repeat_instance"] = instance

# Rename summaryfile headers using map function
summary_df.columns = summary_df.columns.to_series().map(summary_rename_col)

# Add meta_dict as new columns to summary_df.
summary_df = summary_df.assign(**meta_dict)

# Concatenate summary_df index as string and run_name column to a new column.
summary_df["local_id"] = summary_df["run_name"] + "_" + summary_df.index.astype(str)

# Set rapid_local_id, diagnostic_local_id, sequence_local_id, and analysis_local_id to local_id.
summary_df["rapid_local_id"] = summary_df["local_id"]
summary_df["diagnostic_local_id"] = summary_df["local_id"]
summary_df["sequence_local_id"] = summary_df["local_id"]
summary_df["analysis_local_id"] = summary_df["local_id"]

# Set index to local_id.
summary_df.set_index("local_id", inplace=True)

# Assign central_id's, gisaid_name's to summary_df based on last used central_id on REDCap.


# Rename FASTA headers based on new gisaid_name's.



# Write summary_df to file for semi-automated redcap imports (need run separate script to import fastas).
summary_df.to_csv(outfile)


# try, except to terminate script when error raised.