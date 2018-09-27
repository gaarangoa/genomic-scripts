import sys
import click
from Bio import SeqIO
import logging
import gzip
import json


@click.command()
@click.option('--fasta', required=True, help='fasta input file')
@click.option('--entries', required=True, help='tabular file with entries')
def fasta_subset(fasta, entries):
    '''

    Search and retrieve sequences from fasta file

    This script hashes the --entries and traverses the --fasta file until all entries are found.
    The running time depends on the length of the file

    '''

    # file with list of sequences to filter
    finp = {i.strip(): True for i in open(entries)}
    # total_entries = len(finp)
    for record in SeqIO.parse(open(fasta), "fasta"):
        # terminate the program if all reads have been reached.
        # if total_entries <= 0: exit()
        _id = record.id
        if not finp:
            exit()
        try:
            assert(finp[_id])
            print(">"+_id+"\n"+str(record.seq))
        except Exception as e:
            pass
        # total_entries -= 1
