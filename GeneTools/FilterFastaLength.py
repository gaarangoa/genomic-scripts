import click
import os
import random
from Bio import SeqIO
import numpy as np


@click.command()
@click.option('--input-file', default='', help='input fasta file')
@click.option('--minl', default=1000, help='Minimum length of sequences to keep (default: 1000)')
def FilterFastaLength(input_file, minl):
    '''
    Remove sequences under some length.

    This scrip removes sequences that are under a specified sequence length. Works for any input fasta
    ideally for using when removing short contigs from assembled librariesself.

    '''

    fo = open(input_file+'.minL_'+str(minl)+'.fasta', 'w')

    for record in SeqIO.parse(open(input_file), "fasta"):
        header = record.description
        seq = str(record.seq)
        if len(seq) < minl: continue
        fo.write('>'+header+'\n'+seq+'\n')

