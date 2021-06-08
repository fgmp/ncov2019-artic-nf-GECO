
process collateSummaryCSV {
    
    tag { params.prefix }
    
    publishDir "${params.outdir}", pattern: "${params.prefix}.summary.csv", mode: 'copy'

    input:
    tuple path(qc_csv), path(depth_csv), path(typing_csv)

    output:
    path "${params.prefix}.summary.csv", emit: summary_csv
    
    script:
    """
    #!/usr/bin/env python
	from glob import glob
	import pandas as pd

	qc = pd.read_csv("${qc_csv}", index_col=0)
	depth = pd.read_csv("${depth_csv}", index_col=0)
	typing = pd.read_csv("${typing_csv}", index_col=0)

	tables = [
		qc,
		depth, 
		typing,
		]

	collate = pd.concat(tables, axis='columns')
	collate.to_csv("${params.prefix}.summary.csv")

    """
}

