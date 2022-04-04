#!/usr/bin/env nextflow

// enable dsl2
nextflow.preview.dsl = 2

// import subworkflows
include {concatenate_workflow} from './workflows/concatenate_workflow.nf'
include {nextclade_workflow} from './workflows/nextclade_workflow.nf'
include {pangolin_workflow} from './workflows/pangolin_workflow.nf'
include {csv_process_workflow} from './workflows/csv_process_workflow.nf'

// import modules
include {pangolin_process} from './modules/pangolin_process.nf'
include {nextclade_process} from './modules/nextclade_process.nf'
include {concatenate_process} from './modules/concatenate_process.nf'
include {process_csv} from './modules/process_csv.nf'
include {dummy_process} from './modules/dummy_process.nf'



workflow {
	main:
		dummy_process()
		concatenate_process(dummy_process.out.dummy_output)
		//nextclade_process(concatenate_process.out.concatenated_fasta)
		//pangolin_process(concatenate_process.out.concatenated_fasta)
		//process_csv(nextclade_process.out.nextclade_tsv,pangolin_process.out.lineage_report_csv)
}


