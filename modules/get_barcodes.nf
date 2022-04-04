process get_barcodes {
    
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "*.csv", mode: 'copy'
    
    output:
    path '*.csv', emit: barcodes
    
    script:

    """
    get_barcodes.py ${params.redcap_url} \
                 ${params.redcap_token} \
                 ${params.redcap_local_ids}

    """
}