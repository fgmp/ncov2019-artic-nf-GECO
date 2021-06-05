
include {getAveDepth} from '../modules/depth.nf'
include {mergeDepthCSVs} from '../modules/depth.nf'

workflow coverageDepth {
    take:
      ch_bam

    main:
      getAveDepth(ch_bam)
      mergeDepthCSVs(getAveDepth.out.depth_csv.toList())
}
