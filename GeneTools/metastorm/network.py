import click
import json
import logging
import pandas as pd


def get_scaffolds(path='', database='', sample_name='', scaffolds={}, evalue=1e-5, identity=80, bitscore=100):
    data = pd.read_csv(path, sep="\t", names=['query', 'subject', 'identity', 'length',
                                              'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'])
    data = data[data['evalue'] <= evalue]
    data = data[data['identity'] >= identity]
    data = data[data['bitscore'] >= bitscore]
    print(f'{database} Hits {len(data)}')
    for ix, i in data.iterrows():
        scaffold_id = sample_name+"_.*._"+i['query'].split('_')[1]
        subject = database+"_.*._"+str(i['subject'])
        try:
            scaffolds[scaffold_id].append(subject)
        except:
            scaffolds[scaffold_id] = [subject]


@click.command()
@click.option('--metadata', default='', help='directory where all the genomes have been downloaded (e.g, /genomes/)')
@click.option('--output-file', default='', help='File where to store the fasta format with the requested genes')
@click.option('--tsv', default=False, is_flag=True, help='metadata is a tab separated file [default comma separated file]')
def network(metadata, output_file, tsv):
    '''
        Retrieve genes based on origin

        This script subtract genes from the *.PATRIC.ffn file or *.PATRIC.faa files. By looking at the speciallity genes:

        Antibiotic Resistance, Drug Target, Essential Gene, Human Homolog, Transporter, Virulence Factor.
    '''

    logging.basicConfig(
        filename=output_file + '.log',
        level=logging.DEBUG,
        filemode="w",
        format="%(levelname)s %(asctime)s - %(message)s"
    )
    log = logging.getLogger()
    sep = ','
    if tsv:
        sep = '\t'

    _metadata = pd.read_csv(metadata, sep=sep)
    target_db = {i['database']: i['is_target']
                 for ix, i in _metadata.iterrows()}

    scaffolds = {}
    for ix, i in _metadata.iterrows():
        get_scaffolds(
            path=i['path'],
            database=i['database'],
            scaffolds=scaffolds,
            sample_name=i['sample_name'],
            evalue=i['evalue'],
            identity=i['identity'],
            bitscore=i['bitscore']
        )

    nodes = {}
    edges = {}
    for i in scaffolds.values():
        for ik, k in enumerate(i):
            try:
                nodes[k] += 1
            except:
                nodes[k] = 1
            for il in range(ik+1, len(i)):
                try:
                    edges[(k, i[il])] += 1
                except:
                    edges[(k, i[il])] = 1

    fo = open(f'{output_file}.nodes.tsv', 'w')
    fo.write('Node,Database,Weight\n')
    for i in nodes:
        database, gene = i.split('_.*._')
        fo.write(",".join([gene, database, str(nodes[i])])+'\n')

    fo.close()

    fo = open(f'{output_file}.edges.tsv', 'w')
    fo.write('Source,Target,source_database,target_database,Weight\n')
    for i in edges:
        s_database, s_gene = i[0].split('_.*._')
        t_database, t_gene = i[1].split('_.*._')

        if target_db[s_database] or target_db[t_database]:
            counts = str(edges[i])
            fo.write(
                ",".join([s_gene, t_gene, s_database, t_database, counts])+'\n')

    fo.close()
