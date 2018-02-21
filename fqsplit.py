import sys
from Bio.SeqIO.QualityIO import FastqGeneralIterator

def retrieve(fi='', listf={}):
        fo1 = open(fi.replace("fastq", "").replace("fq","")+"R1.fq", "w")
	fo2 = open(fi.replace("fastq", "").replace("fq","")+"R2.fq", "w")
        for _id,seq,qual in FastqGeneralIterator(open(fi)):
            header = _id.split(' ')[1]
            #print _id, header
            read = '@%s\n%s\n+\n%s' %(_id, seq, qual)
	    if(header[0]=='1'): fo1.write(read+"\n")
	    if(header[0]=='2'): fo2.write(read+"\n")


retrieve(fi=sys.argv[1])
