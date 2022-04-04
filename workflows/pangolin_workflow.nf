include {pangolin_process} from '../modules/pangolin_process.nf'

workflow pangolin_workflow {
	main:
		pangolin_process()
		
}