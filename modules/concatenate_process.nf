// fasta_path = Channel.fromPath("${params.outdir}/articNcovNanopore_prepRedcap_renameFasta/*.fasta")

process concatenate_process {
    
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "*.fasta", mode: 'copy'

    input:
    path(renamed_fasta)
    
    
    output:
    path '*.fasta', emit: concatenated_fasta
    
    

    script:
    //hard coded path for now
    //copy each fasta file that is emitted to work directory
    //cat ${fasta_path} > all_sequences.fasta
    //cat $PWD/fasta_files/PH* > all_sequences.fasta

    """
    #!/bin/bash

    cat ${renamed_fasta} > all_sequences.fasta

    
    """
}