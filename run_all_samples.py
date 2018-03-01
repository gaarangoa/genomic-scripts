import sys
import os

files = [i.split() for i in open(sys.argv[1])][1:]
outdir = sys.argv[3]
indir = sys.argv[2]

for sample,fastq1gz,fastq2gz in files:
    fastq1 = ".".join(fastq1gz.split('.')[:-1])
    fastq2 = ".".join(fastq2gz.split('.')[:-1])
    print('uncompressing files')
    os.system('gunzip -c '+indir+"/"+fastq1gz+" > "+outdir+"/"+fastq1 )
    os.system('gunzip -c '+indir+"/"+fastq2gz+" > "+outdir+"/"+fastq2 )
    print('running chfilter')
    os.system('chfilter remove --paired-1 '+outdir+'/'+fastq1+' --paired-2 '+outdir+'/'+fastq2+' --out-dir '+outdir )
    print('running randomfq')
    os.system('sh randomfq.sh '+outdir+'/'+fastq1+'.no-chl.fastq '+outdir+'/'+fastq2+'.no-chl.fastq 12700000 0')
    print('removing temp files')
    os.system('rm '+outdir+"/"+fastq1+" "+outdir+"/"+fastq2+' '+outdir+"/bowtie*")
    print(':) done!')

    