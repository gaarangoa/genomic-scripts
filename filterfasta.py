import sys
from Bio import SeqIO

'''
    THIS IS A HIGH INTENSIVE PROGRAM, ONLY USE IT IF YOU HAVE A SMALL DATASET!!, the process time is O(NM)
'''

fi=sys.argv[1] # fastafile from besthit
finp = { i.split()[0]: True sys.argv[2] } # file with list of sequences to filter

for record in SeqIO.parse(open(fi), "fasta"):
    id = record.id.split(sep)[0]

    # if the length of the query is zero, close the program
    if not finp: close()

    # traverse all the reads
    for read in finp.values():
        if read in id:
            print(id+"\t"+str(len(record.seq)))
            break

    # remove the read that has been found
    del finp[read]


