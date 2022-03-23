include {nextclade_process} from '../modules/nextclade_process.nf'

workflow nextclade_workflow {
	main:
		nextclade_process()
		
}