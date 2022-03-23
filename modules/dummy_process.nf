process dummy_process {
    
    publishDir "output", pattern: '*.txt', mode: 'copy'

    output:
    file '*.txt', emit: dummy_output

    script:

    """
    echo dummy_process task path: $PWD > dummy.txt
    """
}