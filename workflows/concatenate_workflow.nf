include {concatenate_process} from '../modules/concatenate_process.nf'

workflow concatenate_workflow {
	main:
		concatenate_process()
		
}