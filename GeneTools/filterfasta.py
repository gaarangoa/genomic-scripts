import sys
from Bio import SeqIO

'''
    THIS IS A HIGH INTENSIVE PROGRAM, ONLY USE IT IF YOU HAVE A SMALL DATASET!!, the process time is O(NM)
'''

fi=sys.argv[1] # fastafile from besthit
finp = { i.strip(): True for i in open(sys.argv[2]) } # file with list of sequences to filter

for record in SeqIO.parse(open(fi), "fasta"):
    _id = record.id
    if not finp: exit()
    try:
        finp[_id.replace('_template','')]
        print(">"+_id+"\n"+str(record.seq))
        finp[_id.replace('_template','')]
    except Exception as e:
        pass


