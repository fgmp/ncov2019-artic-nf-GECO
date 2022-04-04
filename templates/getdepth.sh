#!/usr/bin/env bash
# Add if-else or assert statement to check total rows equal to largest coordinate in depth file, otherwise return error
if [[ \$(samtools view ${bam}) ]]
then
    samtools depth -d 1000000 -a ${bam} | awk '{SUM+=\$3} END {OFS=","; print "${sampleName}", SUM/NR}' > ${sampleName}.depth.csv
else
    echo "${sampleName},0" > ${sampleName}.depth.csv
fi
