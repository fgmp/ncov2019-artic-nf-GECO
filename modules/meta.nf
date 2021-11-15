
process makeMeta {

    tag { params.prefix }
    
    publishDir "${params.outdir}", pattern: "${params.prefix}.redcap_meta.csv", mode: 'copy'
    publishDir "${params.outdir}", pattern: "${params.prefix}.redcap_meta_case.csv", mode: 'copy'
    publishDir "${params.outdir}", pattern: "${params.prefix}.redcap_meta_diagnostic.csv", mode: 'copy'
    publishDir "${params.outdir}", pattern: "${params.prefix}.redcap_meta_sequence.csv", mode: 'copy'
    publishDir "${params.outdir}", pattern: "${params.prefix}.redcap_meta_analysis.csv", mode: 'copy'

    input:
    tuple path(summary_csv), path(runparam)

    output:
    path "${params.prefix}.redcap_meta.csv", emit: redcap_meta_csv
    path "${params.prefix}.redcap_meta_case.csv", emit: redcap_meta_case_csv
    path "${params.prefix}.redcap_meta_diagnostic.csv", emit: redcap_meta_diagnostic_csv
    path "${params.prefix}.redcap_meta_sequence.csv", emit: redcap_meta_sequence_csv
    path "${params.prefix}.redcap_meta_analysis.csv", emit: redcap_meta_analysis_csv


    script:  
    if ( params.illumina ) {
       metaSetting = "illumina"
    } else {
       metaSetting = "nanopore"
    }

    """
    make_meta.py ${metaSetting} \
                 ${summary_csv} \
                 ${runparam} \
                 ${params.redcap_dag} \
                 ${params.redcap_instance} \
                 ${params.redcap_url} \
                 ${params.redcap_token} \
                 ${params.prefix}
    """

}
