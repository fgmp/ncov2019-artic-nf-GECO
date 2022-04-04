process pangolin_process {

    conda '/data/apps/miniconda3/envs/cov2'
    
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "*.csv", mode: 'copy'
    
    input:
    path(concatenated_fasta)
    
    output:
    path 'lineage_report.csv', emit: lineage_report_csv
    
    script:

    """
    #!/bin/bash
    
    pangolin --update
    pangolin ${concatenated_fasta}

    """
}
