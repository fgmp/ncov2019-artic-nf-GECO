#!/usr/bin/env python3

import subprocess
import sys
import PySimpleGUI as sg
import pathlib
import os

def main():

    working_directory = '/mnt/c'

    sg.theme('DarkTeal7')

    layout = [  
                [sg.Text('API TOKEN:'), sg.In(size=(62,1), enable_events=True ,key='-api_token-')],
                [sg.Output(size=(90,30))],
                [sg.Button('UPLOAD')] ]

    window = sg.Window('UPLOAD CONSENSUS FILES TO REDCAP', layout)

    while True:             # Event Loop
        event, values = window.Read()
        # print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':  
            break
        elif event == 'UPLOAD':

            command = f'echo "Uploading Consensus Files to Redcap . . . "'
            runCommand(cmd=command, window=window)

            # get api_key from user and run python script to upload fasta files to redcap
            api_token = values['-api_token-']
            command = f'python redcap_import_consensus.py "{api_token}"'
            runCommand(cmd=command, window=window)             
    window.Close()


def runCommand(cmd, timeout=None, window=None):
    """ run shell command
    @param cmd: command to execute
    @param timeout: timeout for command execution
    @param window: the PySimpleGUI window that the output is going to (needed to do refresh on)
    @return: (return code from command, command output)
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None        # yes, a 1-line if, so shoot me

    retval = p.wait(timeout)
    return (retval, output)


if __name__ == '__main__':
    main()
