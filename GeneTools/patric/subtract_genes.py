import click
from Bio import SeqIO
import json


def overlap(intervals):
    sorted_by_lower_bound = sorted(intervals, key=lambda tup: tup[0])
    merged = []

    for higher in sorted_by_lower_bound:
        if not merged:
            merged.append(higher)
        else:
            lower = merged[-1]
            # test for intersection between lower and higher:
            # we know via sorting that lower[0] <= higher[0]
            if higher[0] <= lower[1]:
                upper_bound = max(lower[1], higher[1])
                # replace by merged interval
                # print(lower[0], upper_bound)
                merged[-1][0], merged[-1][1] = (
                    lower[0], upper_bound)
                merged[-1][2] += higher[2]

            else:
                merged.append(higher)
    return merged


@click.command()
@click.option('--input-directory', default='', help='directory where all the genomes have been downloaded (e.g, /genomes/)')
@click.option('--genome-id', default='', help='genome identifier to process (e.g., 83332.12)')
@click.option('--output-file', default='', help='File where to store the fasta format with the requested genes')
@click.option('--property', default='Essential Gene', help='Select genes under this property (e.g., Essential Gene)')
@click.option('--extend', default=0, help='Add at the end of each gene # of nucleoties (default: 0)')
def subtract_genes(input_directory, genome_id, output_file, property, extend):
    '''
        Retrieve genes based on origin

        This script subtract genes from the *.PATRIC.ffn file or *.PATRIC.faa files. By looking at the speciallity genes:

        Antibiotic Resistance, Drug Target, Essential Gene, Human Homolog, Transporter, Virulence Factor.
    '''

    metadata_file = open(input_directory + '/' + genome_id +
                         '/' + genome_id + '.PATRIC.spgene.tab')
    metadata = {}
    for ix, i in enumerate(metadata_file):

        # identify keys
        if ix == 0:
            keys = i.strip().split('\t')
            continue

        entry = i.strip().split('\t')
        item = {keys[hx]: h for hx, h in enumerate(entry)}

        if property in item['property']:
            metadata.update({item['patric_id']: item})

    features = []
    for ix, i in enumerate(open(input_directory + '/' + genome_id + '/' + genome_id + '.PATRIC.features.tab')):
        # identify keys
        if ix == 0:
            keys = i.strip().split('\t')
            continue

        # now get only filtered genes
        entry = i.strip().split('\t')
        item = {keys[hx]: h for hx, h in enumerate(entry)}

        try:
            assert (metadata[item['patric_id']])
            features.append(item)
        except Exception as e:
            pass

    genomes = {}
    for i in features:
        try:
            genomes[i['accession']].append(i)
        except Exception as e:
            genomes[i['accession']] = [i]

    fofasta = open(output_file+'.fasta', 'w')
    # Now: traverse the selected genes and retrieve the sequences
    for record in SeqIO.parse(open(input_directory + '/' + genome_id + '/' + genome_id + '.fna'), "fasta"):
        genome_id = record.id
        genome_data = genomes[genome_id]
        sequence = record.seq

        intervals = []
        for genome in genome_data:
            start = min(int(genome['start']), int(genome['end']))
            end = max(int(genome['start']), int(genome['end']))
            if start - extend > 0:
                start = start - extend
            if len(sequence) - extend > 0:
                end = end + extend

            header = genome['patric_id']+'|'+genome['start']+'|'+genome['end']
            intervals.append([start, end, [header]])

        intervals = overlap(intervals)

        for interval in intervals:
            header = "|".join(
                [">"+genome['genome_id'], genome['accession'], 'start:'+str(interval[0]), 'end:'+str(interval[1]), "["+",".join(interval[2]) + "]"])
            _sequence = sequence[int(interval[0]):int(interval[1])]
            fofasta.write(header+'\n'+str(_sequence)+'\n')

    # print(overlap(intervals))

    json.dump([genomes, metadata], open(output_file+'.json', 'w'))
