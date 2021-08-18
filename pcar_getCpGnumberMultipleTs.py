#!/usr/bin/env python

import os, sys
import subprocess
from twobitreader import TwoBitFile

USAGE = 'USAGE: %s <bedFile> <outputFile> <2bit> <threads>+' %sys.argv[0]

def generate_subscript():
    if not os.path.isfile('tem/tem.py'):

        SubScriptsFHD = open('tem/tem.py', 'w')
        SubScriptsFHD.write("import os, sys\n")
        SubScriptsFHD.write("from twobitreader import TwoBitFile\n")
        SubScriptsFHD.write("\n")
        SubScriptsFHD.write("genome = TwoBitFile(sys.argv[3])\n")
        SubScriptsFHD.write("rfhd = open(sys.argv[2]+'.CpGnumber', 'w')\n")
        SubScriptsFHD.write("bedfhd = open(sys.argv[1])\n")
        SubScriptsFHD.write("for line in bedfhd:\n")
        SubScriptsFHD.write("	line = line.strip().split()\n")
        SubScriptsFHD.write("	try:\n")
        SubScriptsFHD.write("		number = genome[line[0]][int(line[1]):int(line[2])].upper().count('CG')\n")
        SubScriptsFHD.write("	except:\n")
        SubScriptsFHD.write("		number = float('nan')\n")
        SubScriptsFHD.write("	rfhd.write('%s\\t%s\\t%s\\t%s\\n' %(line[0],line[1],line[2],number))\n")
        SubScriptsFHD.write("\n")
        SubScriptsFHD.write("rfhd.close()\n")
        SubScriptsFHD.write("bedfhd.close()\n")
        SubScriptsFHD.write("\n")
        SubScriptsFHD.close()


def main():


    process = int(sys.argv[4])

    # load bed file
    bed = []
    fhd = open(sys.argv[1])
    for line in fhd:
        bed.append(line)
    fhd.close()

    # creat tem dirctory
    os.system('mkdir -p tem')

    # add tem files to dirctory, scripts, bwfiles & bed files
    generate_subscript()

    CMD = "cd tem && ln -s %s ." %(sys.argv[3])
    os.system(CMD)

    # tem bed file
    sub_sizes = int(len(bed) / process)
    sub_index = []
    for i in range(process-1):
        sub_index.append((i*sub_sizes, i*sub_sizes+sub_sizes))
    sub_index.append((process*sub_sizes-sub_sizes,len(bed)))
    for i in range(process):
        tembedfhd = open('tem/tem%d_%s.bed' %((i+1), sys.argv[2]), 'w')
        tembedfhd.write("".join(bed[sub_index[i][0]:sub_index[i][1]]))
        tembedfhd.close()


    processes = []
    for i in range(process):
        CMD = "cd tem && python tem.py tem%d_%s.bed %s_tem_%d %s" %(i+1, sys.argv[2], sys.argv[2], i+1, sys.argv[3])
        # print("Sub Command: ", CMD)
        processes.append(subprocess.Popen(CMD, shell=True))
    stats = []
    for i in range(process):
        stats.append(os.waitpid(processes[i].pid,0))
    CMD = ''
    CMD += "cat "
    for j in range(process):
        CMD += "tem/%s_tem_%d.CpGnumber " %(sys.argv[2], j+1)
    CMD += "| sort -k1,1 -k2,2n > %s.CpGNumber && \\\n" %(sys.argv[2])
    CMD = CMD[:-5]
    rfhd = open('tem.sh', 'w')
    rfhd.write(CMD)
    rfhd.close()
    # print("Cat Command: ", CMD)
    p = subprocess.Popen('bash tem.sh', shell = True)
    try:
        os.waitpid(p.pid, 0)
    except OSError:
        pass
    p = subprocess.Popen('rm -r tem tem.sh', shell = True)
    try:
        os.waitpid(p.pid, 0)
    except OSError:
        pass


# program running
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Info("User interrupts me! ;-) See you!")
        sys.exit(0)
