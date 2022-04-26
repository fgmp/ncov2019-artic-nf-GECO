@echo off
wsl -e bash -lic "conda activate redcap_upload; python upload_fasta.py"
