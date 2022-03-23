#!/home/tohoku/apps/miniconda3/envs/nextflow_conda_sandbox/bin/python

import sys

input_param = sys.argv[1]
input_param = int(input_param)
print(f' input = {input_param}')

if(input_param == 1):
    f = open('helloworld.txt','w')
    f.write('hello world 1')
    f.close()



    
 