import click
from Bio import SeqIO
import logging
import gzip
from ete3 import NCBITaxa
import pandas as pd

@click.command()
@click.option('--taxa-file', required=True, help='taxonomy files separated by comma')
@click.option('--sample-names', required=True, help='sample names separated by comma')
@click.option('--output-file', required=True, help='output table')
@click.option('--taxa-column', default=1, help='column in the taxa file that contains the taxonomy IDs (starts from 0)')

def taxa_file_to_table(taxa_file, sample_names, taxa_column, output_file):
    '''
    Convert files with taxonomy NCBI id to a matrix of counts.

    Tested on centrifuge output

    '''

    logging.basicConfig(
        filename=output_file + '.log',
        filemode="w",
        level=logging.INFO,
        format="%(levelname)s %(asctime)s - %(message)s"
    )
    log = logging.getLogger()

    log.info('Index sequences to subtract from fastq file')
    ncbi = NCBITaxa()

    files = taxa_file.split(",")
    samples = sample_names.split(",")

    log.debug("Input files: %s"%files)
    log.debug("Input samples: %s"%sample_names)

    metadata = [(i, samples[ix]) for ix, i in enumerate(files)]

    taxa_dict = {}
    for taxa_file, sample_name in metadata:
        for item in open(taxa_file):
            taxa_id = item.split()[taxa_column]
            try:
                assert(taxa_dict[taxa_id])
            except Exception as e:
                taxa_dict[taxa_id] = {i: 0 for i in samples}

            lineage = ncbi.get_lineage(int(taxa_id))
            names = ncbi.get_taxid_translator(lineage)

            taxa_dict[taxa_id]['lineage'] = ";".join( [names[taxid] for taxid in lineage] )
            taxa_dict[taxa_id][sample_name] += 1


    _table = pd.DataFrame.from_dict(taxa_dict).transpose()

    _table.index.name = 'out_id'
    log.debug(_table)

    _table.to_csv(output_file, sep="\t")

    metadata = pd.DataFrame.from_dict({i: {'name': i} for i in samples}).transpose()
    metadata.index.name='sample_id'
    metadata.to_csv(output_file+'.metadata.tsv', sep="\t")



