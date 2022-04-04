include {HelloWorldprocess} from '../modules/helloworldprocess.nf'

workflow HelloWorldworkflow {
	main:
		HelloWorldprocess()
		
}