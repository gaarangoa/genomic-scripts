import click
import json
import logging
import pandas as pd
from tqdm import tqdm
import sys

origins = {
    1:'ARGs',
    2:'MGEs',
    4:'MRGs',
    3:'Functional Genes'
}

pathogens = {
    1352: 'Enterococcus faecium',
    1280: 'Staphylococcus aureus',
    573: 'Klebsiella pneumonia',
    470: 'Acinetobacter baumannii',
    287: 'Pseudomonas aeruginosa',
    42895: 'Enterobacter spp.',
    543: 'Enterobacteriaceae',
    1352: 'Enterococcus faecium',
    1280: 'Staphylococcus aureus',
    210: 'Helicobacter pylori',
    205: 'Campylobacter sp',
    590: 'Salmonellae',
    485: 'Neisseria gonorrhoeae',
    1313: 'Streptococcus pneumoniae',
    727: 'Haemophilus influenzae',
    625: 'Shigella sp'
}

def traverse_data(data):
    for read in tqdm(data):
        for gene in read['data']:

            gene['gene_id'] = gene['metadata'][0]
            gene['category'] = gene['metadata'][3]
            gene['gene_name'] = gene['metadata'][4]
            gene['read'] = gene['block_id']

            gene['group'] = origins[gene['origin']]

            if origins[gene['origin']] == 'MRGs':
                gene['gene_name'] = gene['category']

            if origins[gene['origin']] == 'Functional Genes':
                gene['gene_name'] = gene['category']


            gene['NCBI_taxa_id'] = read['read'][0]['taxa_id']
            gene['taxa_centrifuge_score'] = read['read'][0]['taxa_score']
            gene['species'] = read['read'][0]['taxa_species']

            try:
                assert(pathogens[int(gene['NCBI_taxa_id'])])
                gene['is_pathogen'] = 1
            except:
                gene['is_pathogen'] = 0


            del gene['metadata']
            del gene['block_id']
            del gene['color']
            del gene['origin']
            del gene['stroke_width']
            del gene['total_reads']
            del gene['value']
            del gene['score']
            del gene['position']

            yield gene

@click.command()
@click.option('--input-file', default='', help='JSON fil downloaded from NanoARG')
@click.option('--output-file', default='', help='file with the mapping table as shown in the genes mapped to nanopore reads')

def mapping_table(input_file, output_file):
    '''
        Generate table of genes mapped to nanopore reads

        This tool will generate the full table named "genes
        mapped to nanopore reads" under the NanoARG website.

        https://bench.cs.vt.edu/nanoarg/

    '''

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(levelname)s %(asctime)s - %(message)s"
    )
    log = logging.getLogger()

    log.info('loading input file ' + input_file)
    data = json.load(open(input_file))

    log.info('traversing file ' + input_file)
    reads = pd.DataFrame(traverse_data(data[0]))

    dataset = reads[
    [
        'read',
        'gene_id',
        'gene_name',
        'group',
        'category',
        'start',
        'end',
        'strand',
        'identity',
        'bitscore',
        'evalue',
        'NCBI_taxa_id',
        'taxa_centrifuge_score',
        'species',
        'coverage',
        'is_pathogen'
        ]
    ]

    log.info('Storing table to '+ output_file)
    dataset.to_csv(output_file, index=False)