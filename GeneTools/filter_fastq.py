import click
from Bio import SeqIO
import logging
import gzip

@click.command()
@click.option('--qfile', required=True, help='Filter all sequences that contain this taxa id (look at all levels)')
@click.option('--qfilter', required=True, help='input tabular file with sequence ids. File must be a gz compressed file')
@click.option('--outfile', required=True, help='Save fastq file to this filename')
@click.option('--qcolumn', default=0, help='Column where the sequences ids (default: 1)')

def filter_fastq(qfilter, qcolumn, qfile, outfile):
    '''
    Subtract fastq reads from a list of entries.

    This scrip picks up sequences in qfilter (fastq file) from qfile (tabular file where first column corresponds to read id).

    '''

    logging.basicConfig(
        filename=qfile + '.log',
        level=logging.DEBUG,
        format="%(levelname)s %(asctime)s - %(message)s"
    )
    log = logging.getLogger()

    log.info('Index sequences to subtract from fastq file')
    _index = {i.split()[qcolumn]: True for i in open(qfilter)}

    log.info('Traverse fastq file to filter sequences of interest')
    fo = gzip.open(outfile, 'w')
    with gzip.open(qfile, 'rt') as handle:
        for record in SeqIO.parse(handle, "fastq"):
            try:
                assert (_index[record.id])
                fo.write(record.format("fastq"))
            except Exception as e:
                pass



