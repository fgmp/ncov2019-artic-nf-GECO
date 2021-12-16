#!/usr/bin/env python3

import json
import sys
import xml.dom.minidom

import pandas as pd
import redcap

setting = sys.argv[1]
summaryfile = sys.argv[2]
metafile = sys.argv[3]
dag = sys.argv[4]
instance = sys.argv[5]
url = sys.argv[6]
token = sys.argv[7]
outname = sys.argv[8]

# Set key name for the metafile data to be collected.
# Include blank mandatory fields for easy entry & import of more metadata by encoders.
meta_dict = {
    "central_id" : "",
    "redcap_repeat_instrument" : "",
    "redcap_repeat_instance" : "",
    "redcap_data_access_group" : "",
    "local_id" : "",
    "gisaid_name" : "",
    "adm3" : "",
    "adm2" : "",
    "adm1" : "",
    "adm0" : "",
    "date_collected" : "",
    "date_received" : "",
    "sample_type_collected" : "",
    "age" : "",
    "sex" : "",
    "patient_outcome" : "",
    "rapid_local_id" : "",
    "diagnostic_local_id" : "",
    "originating_lab" : "",
    "originating_lab_address" : "",
    "sequence_local_id" : "",
    "project_id" : "",
    "flowcell_id" : "",
    "flowcell_type" : "",
    "instrument_make" : "",
    "instrument_model" : "",
    "run_name" : "",
    "library_seq_kit" : "",
    "library_strategy" : "",
    "analysis_local_id" : "",
    "gisaid_authors" : "",
    "assembly_method" : "",
}

# Set how summaryfile cols are renamed.
summary_rename_col = {
    "pct_covered_bases" : "missing",
    "ave_cov_depth" : "ave_depth",
    "fasta" : "fasta",
}

# Set which summaryfile cols are dropped.
summary_drop_col = [
    "pct_N_bases",
    "longest_no_N_run",
    "num_aligned_reads",
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
        sys.exit("Instrument make/model not recognized from run info file's RunParametersVersion xml node.")

    # Collect metafile Chemistry for library_strategy.
    chemistry_node = str(doc.getElementsByTagName("Chemistry")[0].firstChild.nodeValue)
    if "Amplicon" in chemistry_node:
        meta_dict["library_strategy"] = 0
    else:
        sys.exit("Library strategy not recognized from run info file's Chemistry xml node.")

    # Set redcap_data_access_group value to dag.
    meta_dict["redcap_data_access_group"] = dag

    # Set redcap_repeat_instance value to 1.
    meta_dict["redcap_repeat_instance"] = instance

# Collect metadata for nanopore.
elif setting == "nanopore":
    # Parse txt metafile.
    doc = dict()
    with open(metafile, "r") as f:
        metafile_str = f.read()
        print(metafile_str)
        doc = dict(item.split("=") for item in metafile_str.split("\n") if "=" in item)

    # Set run_name to first half of summary_df index.
    meta_dict["run_name"] = summary_df.index.values[0].split("_barcode")[0]

    # Collect metafile sample_id for project_id.
    meta_dict["project_id"] = doc["sample_id"]

    # Collect metafile flow_cell_id for flowcell_id.
    meta_dict["flowcell_id"] = doc["flow_cell_id"]

    # Collect metafile protocol for flowcell_type.
    meta_dict["flowcell_type"] = doc["protocol"].split(":")[1]

    # Collect metafile instrument for instrument_make and instrument_model.
    instrument_ont = doc["instrument"]
    if "MN" in instrument_ont:
        meta_dict["instrument_make"] = 1
        meta_dict["instrument_model"] = 1
    elif "MC" in instrument_ont:
        meta_dict["instrument_make"] = 1
        meta_dict["instrument_model"] = 0
    else:
        sys.exit("Instrument make/model not recognized from run info file's instrument descriptor.")

    # Set whole genome tiled amplicon as default ont library_strategy.
    meta_dict["library_strategy"] = 0

    # Collect metafile protocol for library_seq_kit.
    meta_dict["library_seq_kit"] = doc["protocol"].split(":")[2]

    # Set redcap_data_access_group value to dag.
    meta_dict["redcap_data_access_group"] = dag

    # Set redcap_repeat_instance value to 1.
    meta_dict["redcap_repeat_instance"] = instance

# Rename summaryfile headers using map function
summary_df.columns = summary_df.columns.to_series().map(summary_rename_col)

# Add meta_dict as new columns to summary_df.
summary_df = summary_df.assign(**meta_dict)

# Obtain local_id from run_name and index for illumina, or index only for nanopore.
if setting == "illumina":
    summary_df["local_id"] = summary_df["run_name"] + "_" + summary_df.index.astype(str)
elif setting == "nanopore":
    summary_df["local_id"] = summary_df.index.astype(str)

# Set rapid_local_id, diagnostic_local_id, sequence_local_id, and analysis_local_id to local_id.
summary_df["rapid_local_id"] = summary_df["local_id"]
summary_df["diagnostic_local_id"] = summary_df["local_id"]
summary_df["sequence_local_id"] = summary_df["local_id"]
summary_df["analysis_local_id"] = summary_df["local_id"]

# NOTE: PyCap API will fail if there are more than 1M cells in the project.
# See robust export func from docs: https://pycap.readthedocs.io/en/latest/deep.html#dealing-with-large-exports
# But above will also fail if there are more than 1M records in the project. Maybe use SQL lib by that point?

## Assign central_id's, gisaid_name's to summary_df based on last used central_id on REDCap.
# Fetch last used central_id from REDCap, set new central_id.
project = redcap.Project(url, token)
fields_of_interest = ['central_id']
central_id_ls = project.export_records(fields=fields_of_interest)
last_central_id = int(central_id_ls[-1]['central_id'])
new_central_id = last_central_id + 1

# Loop summary_df rows.
for index, row in summary_df.iterrows():
    # Set central_id of record to new central_id.
    summary_df.loc[index, "central_id"] = new_central_id
    # Set gisaid_name of record making use of new central_id.
    summary_df.loc[index, "gisaid_name"] = "PH"+"-"+dag.upper()+"-"+str(new_central_id)
    # Increment new central_id.
    new_central_id = new_central_id + 1

# Set summary_df index to central_id.
summary_df.set_index("central_id", inplace=True)

# Separate output csv's by repeat instrument.
# Add mandatory fields for easy entry & import of more metadata by encoders.
# Case instrument
case_cols = ["central_id", "redcap_repeat_instrument", "redcap_repeat_instance",
    "redcap_data_access_group", "local_id", "gisaid_name",
    "adm3", "adm2", "adm1",
    "adm0", "date_collected", "date_received",
    "sample_type_collected", "age", "sex",
    "patient_outcome"
    ]
summary_case_df = summary_df.filter(case_cols, axis=1)
summary_case_df["redcap_repeat_instrument"] = "case"

# Diagnostic instrument
diag_cols = ["central_id", "redcap_repeat_instrument", "redcap_repeat_instance",
    "redcap_data_access_group", "diagnostic_local_id", "originating_lab",
    "originating_lab_address"]
summary_diagnostic_df = summary_df.filter(diag_cols, axis=1)
summary_diagnostic_df["redcap_repeat_instrument"] = "diagnostic"

# Sequence  instrument
seq_cols = ["central_id", "redcap_repeat_instrument", "redcap_repeat_instance",
    "redcap_data_access_group", "sequence_local_id", "project_id",
    "flowcell_id", "flowcell_type", "instrument_make",
    "instrument_model", "run_name", "library_seq_kit" ,
    "library_strategy"]
summary_sequence_df = summary_df.filter(seq_cols, axis=1)
summary_sequence_df["redcap_repeat_instrument"] = "sequence"

# Analysis instrument
analysis_cols = ["central_id", "redcap_repeat_instrument", "redcap_repeat_instance",
    "redcap_data_access_group", "analysis_local_id", "gisaid_authors",
    "assembly_method", "ave_depth", "missing"]
summary_analysis_df = summary_df.filter(analysis_cols, axis=1)
summary_analysis_df["redcap_repeat_instrument"] = "analysis"


# Write summary_df's to file for semi-automated redcap imports.
summary_df.to_csv(outname+".redcap_meta.csv")
summary_case_df.to_csv(outname+".redcap_meta_case.csv")
summary_diagnostic_df.to_csv(outname+".redcap_meta_diagnostic.csv")
summary_sequence_df.to_csv(outname+".redcap_meta_sequence.csv")
summary_analysis_df.to_csv(outname+".redcap_meta_analysis.csv")
