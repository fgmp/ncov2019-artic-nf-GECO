include {process_csv} from '../modules/process_csv.nf'

workflow csv_process_workflow {
	main:
		process_csv()
		
}