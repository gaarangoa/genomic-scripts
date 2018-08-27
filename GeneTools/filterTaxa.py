import click
import os
import random
from Bio import SeqIO
import numpy as np
from ete3 import NCBITaxa
import logging

@click.command()
@click.option('--input-file', required=True, help='input file with read_id and taxa_id')
@click.option('--taxa', required=True, help='Filter all sequences that contain this taxa id (look at all levels)')
@click.option('--update-taxa-db', is_flag=True, help='Update ncbi taxonomy database')
@click.option('--read-pos', default=0, help='column index of read id (default: 0)')
@click.option('--taxa-pos', default=2, help='column index of the taxonomy id (default: 2)')
@click.option('--sep', default="\t", help='separator of file fields (default: tab "\\t")')
def filter_taxa(input_file, taxa, update_taxa_db, read_pos, taxa_pos, sep):
    '''
    Get a list of taxa ID and filter the reads under certain taxa

    For instance: retrieve all sequences that are under the family Enterobacteriaceae (546 taxa id).

    The default values are used for centrifuge output, if you use a different type of file, please specify the column number where the read id is and taxa id.
    You can also use a different separator, by default it uses "\t".

    '''

    logging.basicConfig(
        filename=input_file + '.log',
        level=logging.DEBUG,
        format="%(levelname)s %(asctime)s - %(message)s"
    )
    log = logging.getLogger()

    log.info('Load NCBI taxa database')
    ncbi = NCBITaxa()
    if update_taxa_db:
        log.info('Updating NCBI taxa database')
        ncbi.update_taxonomy_database()

    fo = open(input_file+'.selected.'+taxa+'.tsv', 'w')
    for ix, i in enumerate(open(input_file)):
        if ix == 0: continue
        i = i.strip().split(sep)
        read_id = i[read_pos]
        taxa_id = i[taxa_pos]

        # get lineage of the taxa id
        lineage = ncbi.get_lineage(int(taxa_id))
        try:
            if int(taxa) in lineage:
                fo.write("\t".join([read_id, taxa_id]) + "\n")
        except Exception as inst:
            log.error(str(inst))

    fo.close()







