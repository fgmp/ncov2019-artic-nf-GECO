process process_csv {
    params.meta_analysis_path = ''

    //conda '/home/tohoku/apps/miniconda3/envs/csv_processing'

    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "*.csv", mode: 'copy'
    
    input:
    path(nextclade_tsv) 
    path(lineage_report_csv)
    path(redcap_meta_analysis_csv)

    output:
    file '*.csv'

    script:

    """
    text_join.py ${nextclade_tsv} \
                 ${lineage_report_csv} \
                 ${redcap_meta_analysis_csv} \
                 "${params.gisaid_authors}" \
                 "${params.assembly_method}"
    """
}