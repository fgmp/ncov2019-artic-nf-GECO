process nextclade_process {
    
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "*.tsv", mode: 'copy'

    input:
    path(concatenated_fasta)

    output:
    path 'nextclade.tsv', emit: nextclade_tsv
    
    script:

    """
    nextclade.sh ${concatenated_fasta}
    """
}