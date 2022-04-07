#!/usr/bin/env python3

import pandas as pd
import sys

nextclade_path = sys.argv[1]
pangolin_path = sys.argv[2]
redcap_meta_analysis_path = sys.argv[3]
gisaid_authors = sys.argv[4]
assembly_method = sys.argv[5]

def read_and_sort_csv(analyzer):
    #textjoins the output csv files of the analyzer and output it into a separate csv file
    if analyzer == 'pangolin':
        filename = pangolin_path
        delimiter = ','
        header = 'pangolin_string'
        column1 = 'taxon'
        
    elif analyzer == 'nextclade':
        filename = nextclade_path
        delimiter = '\t'
        header = 'nextclade_string'
        column1 = 'seqName'
        
    string_val = []
    line_count = 0

    # assign dataset
    csvData = pd.read_csv(filename, delimiter=delimiter)

    #rename first column to central_id 
    csvData.rename(columns={column1:'central_id'}, inplace=True)
                                         
    # sort data frame
    csvData.sort_values('central_id', 
                     axis=0,
                     ascending=[True], 
                     inplace=True)

    #print(csvData)
    return csvData

def text_join(data_frame, header):
    string_val = []
    line_count = 0

    for row in data_frame.iterrows():
        row_data = data_frame.iloc[line_count].to_numpy(dtype=str)
        string_val.append("|".join(row_data))
        line_count += 1
    
    text_joined_df = pd.DataFrame(string_val, columns=[header])

    return text_joined_df

def update_column(column,meta_output_df):  
    if column == 'gisaid_authors':
        data = gisaid_authors
    elif column == 'assembly_method':
        data = assembly_method

    for row in range(0,len(meta_output_df)):
        meta_output_df.loc[row, column] = data 
    
    return meta_output_df

nextclade_df = read_and_sort_csv('nextclade')

pangolin_df = read_and_sort_csv('pangolin')

# merge nextclade and pangolin to link central_ids
merged_df = pd.merge(nextclade_df, pangolin_df, 
                on='central_id', 
                how='outer')

# split nextclade and pangolin
nextclade_df = merged_df[list(nextclade_df.columns)]
pangolin_df = merged_df[list(pangolin_df.columns)]

# textjoin nextclade and pangolin
nextclade_df = text_join(nextclade_df, 'nextclade_string')
pangolin_df = text_join(pangolin_df, 'pangolin_string')

# concatenate nextclade and pangolin into one dataframe
merged_df = pd.concat([nextclade_df, pangolin_df], axis=1)
print(merged_df)

# merge meta analysis file and, nextlade and pangolin dataframe.
# assumes meta_analysis file is always sorted by taxon
meta_df = pd.read_csv(redcap_meta_analysis_path, delimiter=',')
meta_output = pd.concat([meta_df, merged_df], axis=1)

#update column of gisaid authors and assembly method
meta_output = update_column('gisaid_authors',meta_output)
meta_output = update_column('assembly_method',meta_output)
print(meta_output)

#save to csv file
meta_output.to_csv('meta_analysis.csv', index=False)
