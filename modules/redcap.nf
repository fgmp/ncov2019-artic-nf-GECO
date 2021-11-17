
process makeMeta {

    tag { params.prefix }

    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "${params.prefix}.redcap_meta.csv", mode: 'copy'
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "${params.prefix}.redcap_meta_case.csv", mode: 'copy'
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "${params.prefix}.redcap_meta_diagnostic.csv", mode: 'copy'
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "${params.prefix}.redcap_meta_sequence.csv", mode: 'copy'
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "${params.prefix}.redcap_meta_analysis.csv", mode: 'copy'

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


process renameFasta {

    tag { sampleName }

    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "*.fasta", mode: 'copy'
    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}", pattern: "redcap_import_consensus.py", mode: 'copy'

    input:
    tuple path(redcap_meta), val(sampleName) , path(consensus_fasta)

    output:
    path "*.fasta", emit: renamed_fasta
    path "redcap_import_consensus.py"

    script:
    """
    rename_fasta.py ${redcap_meta} \
                    ${consensus_fasta}
    
    cp "$baseDir/bin/redcap_import_consensus.py" .
    """

}

