
include {makeMeta} from '../modules/redcap.nf'
include {renameFasta} from '../modules/redcap.nf'
include {pangolin_process} from '../modules/pangolin_process.nf'
include {nextclade_process} from '../modules/nextclade_process.nf'
include {concatenate_process} from '../modules/concatenate_process.nf'
include {process_csv} from '../modules/process_csv.nf'

workflow prepRedcap {
    take:
      ch_summary_csv
      ch_runparam
      ch_consensus
      ch_redcap_local_ids

    // Should produce both master metadata table & renamed fastas.
    // Maybe subworkflow in same file add for uploading by api.
    main:
      makeMeta(ch_summary_csv.combine(ch_runparam).combine(ch_redcap_local_ids))
      renameFasta(makeMeta.out.redcap_meta_csv.combine(ch_consensus))

      //fasta_path = Channel.fromPath("${params.outdir}/articNcovNanopore_prepRedcap_renameFasta/*.fasta")
      concatenate_process(renameFasta.out.renamed_fasta.toSortedList()) //does not output sorted list as nextflow outputs files in an asynchronous manner
		  nextclade_process(concatenate_process.out.concatenated_fasta)
		  pangolin_process(concatenate_process.out.concatenated_fasta)
		  process_csv(nextclade_process.out.nextclade_tsv,pangolin_process.out.lineage_report_csv,makeMeta.out.redcap_meta_analysis_csv)
      

    emit:
      redcap_csv = makeMeta.out.redcap_meta_csv
}


