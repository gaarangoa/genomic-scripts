import sys
import click
from Bio import SeqIO
import logging
import gzip
import json
import time

@click.command()
@click.option('--fasta', required=True, help='fasta input file')
@click.option('--outdir', required=True, help='output directory')
def split_fasta(fasta, outdir):
    '''

    Filter sequences from fasta file

    This script hashes the --entries and traverses the --fasta file until all entries are found.
    The running time depends on the length of the file

    '''
    fo2 = open(fasta+'.list', 'w')
    # total_entries = len(finp)
    for record in SeqIO.parse(open(fasta), "fasta"):
        # terminate the program if all reads have been reached.
        # if total_entries <= 0: exit()
        key = str(int(100000 * time.time()))
        ofile = outdir + '/' + key + '.fasta'
        fo = open(ofile , 'w')
        _id = record.description
        fo.write(">" + _id + "\n" + str(record.seq) + '\n')
        fo.close()
        fo2.write(ofile+"\t"+key+'\n')


