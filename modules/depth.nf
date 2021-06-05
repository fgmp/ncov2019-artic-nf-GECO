
process getAveDepth {

    tag { sampleName }

    publishDir "${params.outdir}/${task.process.replaceAll(":","_")}/depth", pattern: "${sampleName}.depth.csv", mode: 'copy'
      
    input:
    tuple sampleName, path(bam)
    
    output:
    path "${sampleName}.depth.csv", emit: depth_csv
    
    script:
    """
    # add if-else or assert statement to check total rows equal to largest coordinate in depth file, otherwise return error
    samtools depth -d 1000000 -a ${bam} | awk '{SUM+=\$3} END {OFS=","; print "${sampleName}", SUM/NR}' > ${sampleName}.depth.csv
    """
}


process mergeDepthCSVs {
    
    tag { params.prefix }
    
    publishDir "${params.outdir}", pattern: "${params.prefix}.depth_summary.csv", mode: 'copy'

    input:
    path '*.depth.csv'

    output:
    path "${params.prefix}.depth_summary.csv", emit: depth_summary_csv
    
    script:
    """
    echo "sampleID,ave_cov_depth" | cat - *.depth.csv > ${params.prefix}.depth_summary.csv
    """
}

