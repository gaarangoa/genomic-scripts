import sys
import click
from Bio import SeqIO
import logging
import gzip
import json
import re
import numpy as np
import os


def genearte_one_genome(genome='ATCGATATACCA', k=3):

    _genome = genome
    _sentence = split_genome(genome=_genome, k=k)

    return _sentence


def split_genome(genome="ATCGATATACCA", k=3):
    return re.findall('.'*k, genome)


def genearte_genomes(genome='ATCGATATACCA', k=3, words=50):
    sentences = []
    for index in range(0, k):
        _genome = genome[index:]
        _sentence = split_genome(genome=_genome, k=k)
        _fraction = int(len(genome) / k) - len(_sentence)

        if _fraction > 0:
            _sentence.append('')

        sentences.append(np.array(_sentence, dtype="U"))

    return np.array(sentences)


def genome_to_doc(input_file="", kmer=16, label="", f5=""):
    ''' This function transforms a sequence genome to a document of kmers '''

    records = []
    for record in SeqIO.parse(input_file, 'fasta'):
        _genome = str(record.seq).upper()
        _kmer_count = int(len(_genome) / kmer)
        records.append({
            'sentences': genearte_genomes(genome=_genome, k=kmer),
            'id': record.id,
            '_kmer_count': _kmer_count,
            'label': label
        })

    return records


@click.command()
@click.option('--fasta-file', required=True, help='fasta input file')
@click.option('--kmer', default=11, help='kmer length')
@click.option('--out-file', required=True, help='output file with embeddings')
def fasta2trainKmers(fasta_file, kmer, out_file):
    '''

    Convert a fasta file into a word/sentence file.

    This file contains all consecutive kmers from positions
    i, i+1, i+2, ...., i+n where n is the lenght of the kmers.
    In other words it produces consecutieve kmers versions of
    the input sequence.

    '''

    x = genome_to_doc(input_file=fasta_file, kmer=kmer)

    fo = open(out_file, 'w')
    for i in x:
        for j in i['sentences']:
            fo.write(" ".join(j)+'\n')
