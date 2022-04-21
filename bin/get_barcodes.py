#!/usr/bin/env python3

import sys
from tracemalloc import start
import pandas as pd
import redcap

api_url = sys.argv[1]
api_key = sys.argv[2]
#past_barcodes = sys.argv[3]


#past_barcodes = '/mnt/c/Users/Computer/Desktop/projs/geco_run13_2022-02-24/raw/RITM/sarscov_geco_run15/sarscov_geco_run15_030922/20220309_1009_X3_FAR69486_6ee358bb/GECO-RITMBarcodelocalid_DATA_2022-03-10_1529.csv'

def connect_to_subset(api_url, api_key):
    # Connects to and returns subset of project data frame
    # Uses gssotelo Api key
    #api_url = 'http://192.168.20.33/redcap/api/'
    #api_key = 'CA7768C863D7E1A5791BC222E92C3A0C'
    project = redcap.Project(api_url, api_key)
    fields_of_interest = ['ont_barcode', 'local_id']
    subset_df = project.export_records(fields=fields_of_interest)
    #project_df = project.export_records(format='df')
    return subset_df

redcap_df = connect_to_subset(api_url, api_key)

#transform to pandas dataframe
df = pd.DataFrame(redcap_df)

#subset to only barcodes and local_id and central id
barcodes = df[["local_id", "ont_barcode"]]

#get past barcodes
#past_barcodes_df = pd.read_csv(past_barcodes)

#find last local_id of past barcodes
#last_local_id = past_barcodes_df.local_id.iat[-1]
#start_local_id = barcodes.loc[barcodes['local_id'].str.contains(last_local_id, case=False)]
#start_index = start_local_id.index.values[0]

#omit preceding rows
#barcodes = barcodes.drop(barcodes.index[:start_index + 1])
barcodes = barcodes[["ont_barcode", "local_id"]]

#omit index
barcodes=barcodes.set_index('ont_barcode')

#output csv file
barcodes.to_csv('barcode.csv')

# notes on barcodes: makemetadata.py currently uses the barccodes from the latest central id in the database which correspond to the barcodes given by the input raw data,
# this works for the intended purpose of this pipeline however can produce errors in the cental id assignment when running a previous batch 














