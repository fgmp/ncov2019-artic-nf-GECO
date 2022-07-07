process bammix_process {
    
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "*.csv", mode: 'copy'
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "*.pdf", mode: 'copy'
    
    input:
    path(nextclade_tsv)
    path(bam)
    path(bam_index)

    output:
    file '*.csv'
    file '*.pdf'

    script:

    """
    bammix.py ${nextclade_tsv} .
    """
}