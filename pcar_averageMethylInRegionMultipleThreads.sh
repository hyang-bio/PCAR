#!/usr/bin/env bash

bedF=${1}
cgF=${2}
outF=${3}
threads=${4}

# step1. split into multiple(=threads) small files with 
n_row=`cat ${bedF} | wc -l`
para_l=`bc <<< ${n_row}/${threads}+1`
split -l ${para_l} ${bedF} -d -a 3 ${outF}_subfile_

# step2. calculate average DNA methylation for each small file
for file in `ls ${outF}_subfile_*`
do
	grep '^chr' ${file} | awk 'BEGIN{OFS="\t";FS="\t"}{print $1,$2,$3}' > ${file}.tmp && \
	intersectBed -wao -a ${file}.tmp -b ${cgF} > ${file}.all.G && \
	methyl_processing.py ${file}.all.G ${file}.ave &
done # for file end
wait;
cat ${outF}_subfile_*.ave | sort -S100G -k1,1 -k2,2n --parallel=6 > ${outF}
rm ${outF}_subfile_*
