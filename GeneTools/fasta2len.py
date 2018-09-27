import sys
from Bio import SeqIO
import click


@click.command()
@click.option('--fasta-file', required=True, help='fasta input file')
@click.option('--separator', default="|", help='header separator [default: "|" ]')
def fasta2len(fasta_file, separator):
    '''

    Get the lengths of each sequence in a fasta file.

    '''

    for record in SeqIO.parse(open(fasta_file), "fasta"):
        id = record.id.split(separator)[0]
        print(id+"\t"+str(len(record.seq)))
