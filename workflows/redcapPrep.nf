
include {makeMeta} from '../modules/meta.nf'

workflow prepRedcap {
    take:
      ch_summary_csv
      ch_runparam
    
    // Should produce both master metadata table & renamed fastas.
    // Maybe subworkflow in same file add for uploading by api.
    main:
      makeMeta(ch_summary_csv.combine(ch_runparam))

    emit:
      redcap_csv = makeMeta.out.redcap_meta_csv
}
