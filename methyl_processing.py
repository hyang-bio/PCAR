#!/usr/bin/env python

import sys

def region_methylation(region_G_bed, outputF):
	'''
		The methylation level of each annotated genomic region in each sample was measured as
		the number of methylated CpG by the total number of CpG sites.
		Genome Research 2013 Guo.

		Note: Coverage requirment is restricted to each annotated genomic region!!!
	'''
	region_dict = dict()
	inFH = open(region_G_bed, 'r')
	for line in inFH:
		ele = line.strip().split('\t')
		index = '@'.join(ele[0:3])
		if index not in region_dict:
			region_dict[index] = ['NA', 'NA'] # Initiation
			if ele[7]!='.' and ele[8]!='.':
				region_dict[index][0] = int(ele[7]) #total C
				region_dict[index][1] = int(ele[8]) #methyl C
		else:
			region_dict[index][0] += int(ele[7]) #total C
			region_dict[index][1] += int(ele[8]) #methyl C
	inFH.close()

	outFH = open(outputF, 'w')
	for key in region_dict:
		location = key.split('@')
		if region_dict[key][0]!='NA' and region_dict[key][1]!='NA':
			if region_dict[key][0]>=3:
				outFH.write('%s\t%s\t%s\t%s\n'%(location[0],location[1],location[2],float(region_dict[key][1])/float(region_dict[key][0])))
			else:
				outFH.write('%s\t%s\t%s\t%s\n'%(location[0],location[1],location[2],'NA'))
		else:
			outFH.write('%s\t%s\t%s\t%s\n'%(location[0],location[1],location[2],'NA'))
	outFH.close()


def main():
	region_methylation(sys.argv[1], sys.argv[2])

main()
