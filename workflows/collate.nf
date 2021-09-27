
include {collateSummaryCSV} from '../modules/collate.nf'

workflow collateSummary {
    take:
      ch_qc
      ch_depth

    main:
      collateSummaryCSV(ch_qc.mix(ch_depth).toList())
}
