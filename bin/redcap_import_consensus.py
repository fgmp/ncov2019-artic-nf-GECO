#modules required
import os

import pandas
import redcap
import requests

#read redcap project and export records to be stored as pandas dataframe
proj = redcap.Project('https://geco.ritm-edc.net/redcap/api/', 'INSERT_TOKEN_HERE')
proj_df = proj.export_records(format='df')

#make dictionary to get gisaid_name from central id, dropping rows with nan's for gisaid_name
virusname_dict = proj_df.gisaid_name.dropna().to_dict()

#loop through central ids and import fasta file (named according to gisaid_name) to that record
for i in virusname_dict.keys():
    if type(virusname_dict[i]) == str: #skip records with no gisaid_name
        file_path = './' + str(virusname_dict[i]) + '.fasta'
        if os.path.isfile(file_path): #check if file_path exists. TODO: check if record already has consensus file uploaded.
            data = {
                'token': 'INSERT_TOKEN_HERE',
                'content': 'file',
                'action': 'import',
                'record': str(i),
                'field': 'consensus',
                'returnFormat': 'csv'
            }
            file_obj = open(file_path, 'rb')
            r = requests.post('https://geco.ritm-edc.net/redcap/api/',data=data,files={'file':file_obj})
            file_obj.close()

