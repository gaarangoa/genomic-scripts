import sys
import click
from Bio import SeqIO
import logging
import gzip
import json


def split_genome(genome="ATCGATATACCA", k=3):
    return re.findall('.'*k, genome)

def genearte_one_genome(genome='ATCGATATACCA', k=3):

    _genome = genome
    _sentence = split_genome(genome=_genome, k=k)

    return np.array(_sentence, dtype="U")

@click.command()
@click.option('--fasta-file', required=True, help='fasta input file')
@click.option('--kmer', required=True, help='kmer length')
@click.option('--output-file', required=True, help='output file with embeddings')
def fasta2kmers(fasta_file, kmer, fasttext_model, out_file):
    '''

    Convert a fasta file into an embedding matrix of N size using fasttext

    '''

    # traverse the fasta file
    fo = open(out_file + '.setences', 'w')
    fo2 = open(out_file + '.headers', 'w')

    for record in SeqIO.parse(fasta_file, 'fasta'):
        _genome = str(record.seq).upper()
        fo.write(" ".join(genearte_one_genome(genome=_genome, k=kmer)) + '\n')
        fo2.write(record.description + '\n')
