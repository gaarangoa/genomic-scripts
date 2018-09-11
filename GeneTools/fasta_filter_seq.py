import sys
import click
from Bio import SeqIO
import logging
import gzip
import json

@click.command()
@click.option('--fasta', required=True, help='fasta input file')
@click.option('--entries', required=True, help='tabular file with entries')
def fasta_filter_seq(fasta, entries):
    '''

    Remove the sequences in --entries from --fasta

    '''

    finp = { i.strip(): True for i in open(entries) } # file with list of sequences to filter
    # total_entries = len(finp)
    for record in SeqIO.parse(open(fasta), "fasta"):
        # terminate the program if all reads have been reached.
        # if total_entries <= 0: exit()
        _id = record.id
        if not finp: exit()
        try:
            # is the sequence in the hash table?
            assert(finp[_id.replace('_template','')])
        except Exception as e:
            print(">"+_id+"\n"+str(record.seq))


