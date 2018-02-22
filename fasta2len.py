import sys
from Bio import SeqIO


fi=sys.argv[1] # fastafile from besthit
sep = sys.argv[2] # separator to get only sequence id

for record in SeqIO.parse(open(fi), "fasta"):
    id = record.id.split(sep)[0]
    print(">"+id+"\t"+str(len(record.seq)))

