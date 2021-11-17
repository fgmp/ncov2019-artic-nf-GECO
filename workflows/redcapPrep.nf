
include {makeMeta} from '../modules/redcap.nf'
include {renameFasta} from '../modules/redcap.nf'

workflow prepRedcap {
    take:
      ch_summary_csv
      ch_runparam
      ch_consensus

    // Should produce both master metadata table & renamed fastas.
    // Maybe subworkflow in same file add for uploading by api.
    main:
      makeMeta(ch_summary_csv.combine(ch_runparam))
      renameFasta(makeMeta.out.redcap_meta_csv.combine(ch_consensus))

    emit:
      redcap_csv = makeMeta.out.redcap_meta_csv
}
