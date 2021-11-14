
process makeMeta {

    tag { params.prefix }
    
    publishDir "${params.outdir}", pattern: "${params.prefix}.redcap_meta.csv", mode: 'copy'

    input:
    tuple path(summary_csv), path(runparam)

    output:
    path "${params.prefix}.redcap_meta.csv", emit: redcap_meta_csv

    script:  
    if ( params.illumina ) {
       metaSetting = "illumina"
    } else {
       metaSetting = "nanopore"
    }

    """
    make_meta.py ${metaSetting} ${summary_csv} ${runparam} ${params.redcap_dag} ${params.redcap_instance} ${params.prefix}
    """

}
