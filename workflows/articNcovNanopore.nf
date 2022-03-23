// ARTIC ncov workflow

// enable dsl2
nextflow.preview.dsl = 2

// import modules
include {articDownloadScheme} from '../modules/artic.nf' 
include {articGuppyPlex} from '../modules/artic.nf' 
include {articMinIONNanopolish} from  '../modules/artic.nf' 
include {articMinIONMedaka} from  '../modules/artic.nf'
include {articRemoveUnmappedReads} from '../modules/artic.nf' 
include {makeQCCSV} from '../modules/qc.nf'
include {writeQCSummaryCSV} from '../modules/qc.nf'
include {bamToCram} from '../modules/out.nf'
include {collateSamples} from '../modules/upload.nf'





// import subworkflows
include {Genotyping} from './typing.nf'
include {coverageDepth} from './depth.nf'
include {collateSummary} from './collate.nf'
include {prepRedcap} from './redcapPrep.nf'

// workflow component for artic pipeline
workflow sequenceAnalysisNanopolish {
    take:
      ch_runFastqDirs
      ch_fast5Pass
      ch_seqSummary
    
    main:
      articDownloadScheme()
      
      articGuppyPlex(ch_runFastqDirs.flatten())

      articMinIONNanopolish(articGuppyPlex.out.fastq
                                          .filter{ it.countFastq() > params.minReadsArticGuppyPlex }
                                          .combine(articDownloadScheme.out.scheme)
                                          .combine(ch_fast5Pass)
                                          .combine(ch_seqSummary))

      articRemoveUnmappedReads(articMinIONNanopolish.out.mapped)

      makeQCCSV(articMinIONNanopolish.out.ptrim
                                     .join(articMinIONNanopolish.out.consensus_fasta, by: 0)
                                     .combine(articDownloadScheme.out.reffasta))

      makeQCCSV.out.csv.splitCsv()
                       .unique()
                       .branch {
                           header: it[-1] == 'qc_pass'
                           fail: it[-1] == 'FALSE'
                           pass: it[-1] == 'TRUE'
                       }
                       .set { qc }

     writeQCSummaryCSV(qc.header.concat(qc.pass).concat(qc.fail).toList())

     collateSamples(qc.pass.map{ it[0] }
                           .join(articMinIONNanopolish.out.consensus_fasta, by: 0)
                           .join(articRemoveUnmappedReads.out))

     if (params.outCram) {
        bamToCram(articMinIONNanopolish.out.ptrim.map{ it[0] } 
                        .join (articDownloadScheme.out.reffasta.combine(ch_preparedRef.map{ it[0] })) )

      }


    emit:
      qc_pass = collateSamples.out
      reffasta = articDownloadScheme.out.reffasta
      vcf = articMinIONNanopolish.out.vcf
      bam = articMinIONNanopolish.out.ptrim
      qc_csv = writeQCSummaryCSV.out.qcsummary
      consensus = articMinIONNanopolish.out.consensus_fasta

}

workflow sequenceAnalysisMedaka {
    take:
      ch_runFastqDirs

    main:
      articDownloadScheme()

      articGuppyPlex(ch_runFastqDirs.flatten())

      articMinIONMedaka(articGuppyPlex.out.fastq
                                      .filter{ it.countFastq() > params.minReadsArticGuppyPlex }
                                      .combine(articDownloadScheme.out.scheme))

      articRemoveUnmappedReads(articMinIONMedaka.out.mapped)

      makeQCCSV(articMinIONMedaka.out.ptrim.join(articMinIONMedaka.out.consensus_fasta, by: 0)
                           .combine(articDownloadScheme.out.reffasta))

      makeQCCSV.out.csv.splitCsv()
                       .unique()
                       .branch {
                           header: it[-1] == 'qc_pass'
                           fail: it[-1] == 'FALSE'
                           pass: it[-1] == 'TRUE'
                       }
                       .set { qc }

     writeQCSummaryCSV(qc.header.concat(qc.pass).concat(qc.fail).toList())

     collateSamples(qc.pass.map{ it[0] }
                           .join(articMinIONMedaka.out.consensus_fasta, by: 0)
                           .join(articRemoveUnmappedReads.out))

     if (params.outCram) {
        bamToCram(articMinIONMedaka.out.ptrim.map{ it[0] } 
                        .join (articDownloadScheme.out.reffasta.combine(ch_preparedRef.map{ it[0] })) )

      }
    emit:
      qc_pass = collateSamples.out
      reffasta = articDownloadScheme.out.reffasta
      vcf = articMinIONMedaka.out.vcf

}


workflow articNcovNanopore {
    take:
      ch_fastqDirs
      ch_runparam
      ch_redcap_local_ids
    
    main:
      if ( params.nanopolish ) {
          Channel.fromPath( "${params.fast5_pass}" )
                 .set{ ch_fast5Pass }

          Channel.fromPath( "${params.sequencing_summary}" )
                 .set{ ch_seqSummary }

          sequenceAnalysisNanopolish(ch_fastqDirs, ch_fast5Pass, ch_seqSummary)

          sequenceAnalysisNanopolish.out.vcf.set{ ch_nanopore_vcf }

          sequenceAnalysisNanopolish.out.reffasta.set{ ch_nanopore_reffasta }

      } else if ( params.medaka ) {
          sequenceAnalysisMedaka(ch_fastqDirs)

          sequenceAnalysisMedaka.out.vcf.set{ ch_nanopore_vcf }

          sequenceAnalysisMedaka.out.reffasta.set{ ch_nanopore_reffasta }
      }

      if ( params.gff ) {
          Channel.fromPath("${params.gff}")
                 .set{ ch_refGff }

          Channel.fromPath("${params.yaml}")
                 .set{ ch_typingYaml }

          Genotyping(ch_nanopore_vcf, ch_refGff, ch_nanopore_reffasta, ch_typingYaml)

      }

      // Get average coverage depth for nanopolish
      coverageDepth(sequenceAnalysisNanopolish.out.bam)

      // Collate summary CSV for nanopolish
      collateSummary(sequenceAnalysisNanopolish.out.qc_csv, coverageDepth.out.depth_csv)

      // Prepare metadata & fasta for REDCap import for nanopolish
      prepRedcap(collateSummary.out.summary_csv, ch_runparam, sequenceAnalysisNanopolish.out.consensus, ch_redcap_local_ids)
}

