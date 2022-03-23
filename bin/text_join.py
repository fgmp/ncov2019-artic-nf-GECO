#!/usr/bin/env python3

import pandas as pd
import sys

# definition of arguments
nextclade_path = sys.argv[1]
pangolin_path = sys.argv[2]
redcap_meta_analysis_path = sys.argv[3]
gisaid_authors = sys.argv[4]
assembly_method = sys.argv[5]


def process_csv(analyzer):
    #textjoins the output csv files of the analyzer and output it into a separate csv file
    if analyzer == 'pangolin':
        filename = pangolin_path
        delimiter = ','
        header = 'pangolin_string'
        #output_file = 'pangolin_string.csv'
        #column1 = 'taxon'
        
    elif analyzer == 'nextclade':
        filename = nextclade_path
        delimiter = '\t'
        header = 'nextclade_string'
        #output_file = 'nextclade_string.csv'
        #column1 = 'seqName'
        
    string_val = []
    line_count = 0

    # assign dataset
    csvData = pd.read_csv(filename, delimiter=delimiter, header=None)
    print(csvData)
                                         
    # sort data frame
    csvData.sort_values([0], 
                    axis=0,
                    ascending=[True], 
                    inplace=True)
    
    #textjoin each row in the data frame
    for row in csvData.iterrows():
        if line_count == 0:
            string_val.append(header)
            line_count += 1
            
        else:
            row_data = csvData.iloc[line_count-1].to_numpy(dtype=str)
            string_val.append("|".join(row_data))
            line_count += 1
    
    #write textjoined values to new csv
    df = pd.DataFrame(string_val)
    return df

def update_column(column,meta_output_df):  
    if column == 'gisaid_authors':
        column_index = 5
        data = gisaid_authors
    elif column == 'assembly_method':
        column_index = 6
        data = assembly_method

    for row in range(1,len(meta_output_df)):
        meta_output_df.loc[row, column_index] = data 
    
    return meta_output_df
    

#Merge pangolin and nextclade into one dataframe
merged_df = pd.concat([process_csv('pangolin'), process_csv('nextclade')], axis=1)

#merge meta analysis file and, nextlade and pangolin dataframe.
#assumes meta_analysis file is always sorted by taxon
meta_df = pd.read_csv(redcap_meta_analysis_path, delimiter=',',header=None)
meta_output = pd.concat([meta_df, merged_df], axis=1)

#update column of gisaid authors and assembly method
meta_output = update_column('gisaid_authors',meta_output)
meta_output = update_column('assembly_method',meta_output)

#save to csv file
meta_output.to_csv('meta_output.csv',header=False, index=False)








