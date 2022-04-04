import java.nio.file.Paths

def makeFastqSearchPath ( illuminaPrefixes, illuminaSuffixes, fastq_exts ) {

    def fastqSearchPath = []

    for (suff in illuminaSuffixes){
        for(ext in fastq_exts){
          if ( illuminaPrefixes ) {
            for (prefix in illuminaPrefixes) {
              
              // Make a glob to recurse directories
              dirNameGlob = params.directory.replaceAll(/\/+$/, "") + '**'
 
              // Make a filename glob
              fileNameGlob = prefix + suff + ext

              // Build a path
              searchPath = Paths.get(dirNameGlob, fileNameGlob )

              fastqSearchPath.add(searchPath.toString())
              }
          } else {

              // Make a glob to recurse directories
              dirNameGlob = params.directory.replaceAll(/\/+$/, "") + '**'

              // Make a glob for filenames
              fileNameGlob = suff + ext

              // Build a path
              searchPath = Paths.get(dirNameGlob, fileNameGlob)

              fastqSearchPath.add(searchPath.toString())
          }
        }
    }

    return fastqSearchPath
}


def makeRunParamSearchPath ( runparam ) {

    def runparamSearchPath = ""

    for (inf in runparam){

      // Make a glob to recurse directories
      dirNameGlob = params.directory.replaceAll(/\/+$/, "") + '**'

      // Make a filename glob
      fileNameGlob = inf

      // Build a path
      searchPath = Paths.get(dirNameGlob, fileNameGlob )

      runparamSearchPath = searchPath.toString()
    }

    return runparamSearchPath
}