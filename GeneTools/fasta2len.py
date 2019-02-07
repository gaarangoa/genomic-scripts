import sys
from Bio import SeqIO
import click


@click.command()
@click.option('--fasta-file', required=True, help='fasta input file')
@click.option('--separator', default="|", help='header separator [default: "|" ]')
@click.option('--label-postition', default=0, help='label position [default: 0 ]')

def fasta2len(fasta_file, separator, label_position):
    '''

    Get the lengths of each sequence in a fasta file.

    Write to stout

    '''
    data = {}
    for record in SeqIO.parse(open(fasta_file), "fasta"):
        id = record.id.split(separator)[label_position]
        try:
            data[id]+=len(record.seq)
        except Exception as e:
            data[id] = len(record.seq)

    for i in data:
        print(i+'\t'+str(data[i]))

