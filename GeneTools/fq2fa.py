
import sys
from Bio.SeqIO.QualityIO import FastqGeneralIterator


def retrieve(fi='', listf={}):
    fo = open(fi.replace("fastq", "").replace("fq", "")+"fasta", "w")
    for _id, seq, qual in FastqGeneralIterator(open(fi)):
        header = _id.split(' ')[0]
        read = '>%s\n%s' % (_id, seq)
        fo.write(read+"\n")


retrieve(fi=sys.argv[1])
