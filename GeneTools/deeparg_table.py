import click
from Bio import SeqIO
import logging
import gzip
from ete3 import NCBITaxa
import pandas as pd

@click.command()
@click.option('--deeparg-files', required=True, help='deeparg files separated by comma')
@click.option('--sample-names', required=True, help='sample names separated by comma')
@click.option('--output-file', required=True, help='output table')
@click.option('--counts', is_flag=True, default=False, help="report table with counts instead of 16s normalized [default False]")
@click.option('--header', is_flag=True, default=True, help="First line of the file is the file header [default True]")
def deeparg_table(deeparg_files, sample_names, output_file, counts, header):
    '''

    From the deepARG resutls build a table for analysis.

    '''

    logging.basicConfig(
        filename=output_file + '.log',
        filemode="w",
        level=logging.DEBUG,
        format="%(levelname)s %(asctime)s - %(message)s"
    )
    log = logging.getLogger()

    log.info("Starting")

    files = deeparg_files.split(",")
    samples = sample_names.split(",")

    log.debug("Input files: %s"%files)
    log.debug("Input samples: %s"%sample_names)

    metadata = [(i, samples[ix]) for ix, i in enumerate(files)]

    if not counts:
        index_abn = 2
    else:
        index_abn = 1

    abundance_dict = {}
    for deeparg_file, sample_name in metadata:
        for ix, item in enumerate(open(deeparg_file)):
            if ix == 0 and header: continue
            arg_id = item.split()[0]
            try:
                assert(abundance_dict[arg_id])
            except Exception as e:
                abundance_dict[arg_id] = {i: 0 for i in samples}

            abundance_dict[arg_id][sample_name] += float(item.split()[index_abn])


    _table = pd.DataFrame.from_dict(abundance_dict).transpose()

    _table.index.name = 'category'
    log.debug(_table)

    _table.to_csv(output_file, sep="\t")

