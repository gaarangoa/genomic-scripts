import click
import os
import random
from Bio import SeqIO
import numpy as np


@click.command()
@click.option('--input-file', default='', help='input fasta file')
@click.option('--fr', default=0.2, help='fraction of sequences to get randomly (default: 0.2)')
def fasta2rand(input_file, fr):
    '''
    Retrieve random sequences from a fasta file.
    '''

    total_reads = 0
    for record in SeqIO.parse(open(input_file), "fasta"):
        total_reads += 1

    reads_to_subtract = int(total_reads * fr)

    selected_reads = [i for i in range(total_reads)]
    random.shuffle(selected_reads)
    selected_reads = {i: True for i in selected_reads[:reads_to_subtract]}

    fo = open(input_file+'.sel_'+str(reads_to_subtract)+'.fasta', 'w')
    index = 0
    for record in SeqIO.parse(open(input_file), "fasta"):
        try:
            assert (selected_reads[index])
            header = record.description
            seq = str(record.seq)
            fo.write('>'+header+'\n'+seq+'\n')
        except Exception as e:
            pass
        index += 1
