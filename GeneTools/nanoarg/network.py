import click
import json
import logging
import pandas as pd
from tqdm import tqdm
import sys
import networkx as nx

origins = {
    1: 'ARGs',
    2: 'MGEs',
    4: 'MRGs',
    3: 'Functional Genes'
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


def format_gene(gene):
    gene['gene_id'] = gene['metadata'][0]
    gene['category'] = gene['metadata'][3]
    gene['gene_name'] = gene['metadata'][4]
    gene['read'] = gene['block_id']

    gene['group'] = origins[gene['origin']]

    if origins[gene['origin']] == 'MRGs':
        gene['gene_name'] = gene['category']

    if origins[gene['origin']] == 'Functional Genes':
        gene['gene_name'] = gene['category']

    return gene


def get_node_edges(genes):
    if len(genes) > 1:
        for ix, source in enumerate(genes[:-1]):
            source = format_gene(source)
            for _, target in enumerate(genes[ix + 1:]):
                target = format_gene(target)
                yield {
                    'source': source['gene_name'],
                    'target': target['gene_name'],
                    'source_group': source['group'],
                    'target_group': target['group'],
                }


def get_taxa(read):
    gene = {}
    gene['NCBI_taxa_id'] = read['read'][0]['taxa_id']
    gene['taxa_centrifuge_score'] = read['read'][0]['taxa_score']
    gene['species'] = read['read'][0]['taxa_species']

    try:
        assert(pathogens[int(gene['NCBI_taxa_id'])])
        gene['is_pathogen'] = 'Yes'
    except:
        gene['is_pathogen'] = 'No'

    return gene


def build_network(data):
    network = {}
    for read in tqdm(data):
        taxa = get_taxa(read)
        for edge in get_node_edges(read['data']):
            edge['is_pathogen'] = taxa['is_pathogen']
            try:
                network['{}_{}'.format(
                    edge['source'], edge['target'])]['weight'] += 1
            except:
                network['{}_{}'.format(edge['source'], edge['target'])] = edge
                network['{}_{}'.format(
                    edge['source'], edge['target'])]['weight'] = 1

            try:
                network['{}_{}'.format(
                    edge['source'], taxa['NCBI_taxa_id']
                )]['weight'] += 1
            except:
                network['{}_{}'.format(
                    edge['source'], taxa['NCBI_taxa_id']
                )] = {
                    'source': edge['source'],
                    'source_group': edge['source_group'],
                    'target': taxa['NCBI_taxa_id']+'|'+taxa['species'],
                    'target_group': 'Taxonomy',
                    'weight': 1,
                    'is_pathogen': edge['is_pathogen']
                }

            try:
                network['{}_{}'.format(
                    edge['target'], taxa['NCBI_taxa_id']
                )]['weight'] += 1
            except:
                network['{}_{}'.format(
                    edge['target'], taxa['NCBI_taxa_id']
                )] = {
                    'source': edge['target'],
                    'source_group': edge['target_group'],
                    'target': taxa['NCBI_taxa_id']+'|'+taxa['species'],
                    'target_group': 'Taxonomy',
                    'weight': 1,
                    'is_pathogen': edge['is_pathogen']
                }

    return network.values()


@click.command()
@click.option('--input-file', default='', help='JSON fil downloaded from NanoARG')
@click.option('--output-file', default='', help='file with the mapping table as shown in the genes mapped to nanopore reads')
def network(input_file, output_file):
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
    dataset = pd.DataFrame(build_network(data[0]))

    log.info('Storing table to ' + output_file)
    dataset.to_csv(output_file, index=False)
