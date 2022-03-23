params.input = ''

process HelloWorldprocess {
    
    publishDir "output", pattern: '*.txt', mode: 'copy'

    output:
    file '*.txt'

    script:

    """
    HelloWorld.py ${params.input}
    """
}