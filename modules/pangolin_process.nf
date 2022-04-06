process pangolin_process {

    conda '/data/apps/miniconda3/envs/pangolin'
    
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "*.csv", mode: 'copy'
    
    input:
    path(concatenated_fasta)
    
    output:
    path 'lineage_report.csv', emit: lineage_report_csv
    
    script:

    """
    #!/bin/bash
    
    pangolin --update
    pip install git+https://github.com/cov-lineages/pangolin-data.git
    pangolin ${concatenated_fasta}

    """
}
