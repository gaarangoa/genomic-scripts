import sys
from Bio import SeqIO
import click


@click.command()
@click.option('--fasta-file', required=True, help='fasta input file')
@click.option('--separator', default="|", help='header separator [default: "|" ]')
@click.option('--label', default=0, help='label position [default: 0 ]')

def fasta2len(fasta_file, separator, label):
    '''

    Get the lengths of each sequence in a fasta file.

    Write to stout

    '''
    data = {}
    for record in SeqIO.parse(open(fasta_file), "fasta"):
        id = record.id.split(separator)[label]
        try:
            data[id]['len'] += len(record.seq)
            data[id]['count'] += 1
        except Exception as e:
            data[id] = {"len": len(record.seq), "count": 1}

    for i in data:
        print(i+'\t'+str(data[i]['len']/data[i]['count']))

