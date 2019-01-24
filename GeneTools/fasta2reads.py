import sys
import click
from Bio import SeqIO
import logging
import gzip
import json
import random


@click.command()
@click.option('--fasta', required=True, help='fasta input file')
@click.option('--read-length', default=100, help='length of the reads to generate')
@click.option('--min-sread', default=1, help='minimum reads per sequence')
@click.option('--max-sread', default=10, help='maximum reads per sequence')
def fasta2reads(fasta, read_length, min_sread, max_sread):
    '''

    From a fasta file build a set of random reads

    This script will take an input a fasta file and for each
    sequence will take between the min-sread number of reads to
    the max-sreads maximum number of reads.

    reads are picked up at random positions in the sequence

    '''
    fo = open(fasta.replace('.fasta', '').replace('.fa', '') +
              '.reads.'+str(read_length)+'.fasta', 'w')
    for record in SeqIO.parse(open(fasta), "fasta"):
        # discard sequences that are smaller than read length.
        if len(record.seq) <= read_length:
            continue

        for iread, read in enumerate(range(0, random.randint(min_sread, max_sread))):
            random_position = random.randint(
                0, len(record.seq) - read_length-1)
            read_sequence = record.seq[random_position:random_position + read_length]
            fo.write(">"+record.id+'|'+str(iread)+'\n'+str(read_sequence)+'\n')
