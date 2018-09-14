import click
import os
import random
from Bio import SeqIO
import numpy as np


def random_base(reference, amino):
    if amino:
        bases = {'A': 1, 'R': 2, 'N': 3, 'D': 4, 'C': 5, 'Q': 6, 'E': 7, 'G': 8, 'H': 9, 'I': 10,
                 'L': 11, 'K': 12, 'M': 13, 'F': 14, 'P': 15, 'S': 16, 'T': 17, 'W': 18, 'Y': 19, 'V': 20}
    else:
        bases = {'A': 1, 'C': 2, 'T': 3, 'G': 4}
    try:
        del bases[reference.upper()]
    except:
        pass

    rbases = [i for i in bases.keys()]
    random.shuffle(rbases)
    return rbases[0]


def num_to_base(reference, amino):
    if amino:
        bases = {1: 'A', 2: 'R', 3: 'N', 4: 'D', 5: 'C', 6: 'Q', 7: 'E', 8: 'G', 9: 'H', 10: 'I',
                 11: 'L', 12: 'K', 13: 'M', 14: 'F', 15: 'P', 16: 'S', 17: 'T', 18: 'W', 19: 'Y', 20: 'V'}
    else:
        bases = {1: 'A', 2: 'C', 3: 'T', 4: 'G'}
    return bases[reference]


def insert(sequence, positions, max_indel_size, amino):
    opts = [i for i in range(1, max_indel_size+1)]

    for pos in positions:
        random.shuffle(opts)
        num_indel = opts[0]
        indel = "".join([num_to_base(random.randint(1, 4), amino)
                         for _ in range(num_indel)])

        sequence[pos] = indel

    return sequence


def delete(sequence, positions, max_indel_size, amino):
    opts = [i for i in range(1, max_indel_size+1)]

    for ix, pos in enumerate(positions):
        random.shuffle(opts)
        num_indel = opts[0]
        try:
            del sequence[pos-ix:num_indel+pos-ix]
        except:
            pass
    return sequence


def mismatch(sequence, positions, amino):
    for pos in positions:
        reference = sequence[pos]
        sequence[pos] = random_base(reference, amino)
    return sequence


@click.command()
@click.option('--input-file', default='', help='input fasta file to mutate fasta file')
@click.option('--mutations', default=10, help='percentage of mutations in the sequence (default: 5%)')
@click.option('--insertions', default=30, help='percentage of insertions out of the total mutations (default: 30%)')
@click.option('--deletions', default=30, help='percentage of deletions out of the total mutations (default: 30%)')
@click.option('--mismatches', default=40, help='percentage of mismatches out of the total mutations (default: 40%)')
@click.option('--max-indel-size', default=5, help='maximum indel size (default: 5)')
@click.option('--prefix', default='0', help='prefix added to output file')
@click.option('--prot', default=False, is_flag=True, help='aminoacid sequences')
def mutate(input_file, insertions, deletions, mismatches, mutations, max_indel_size, prefix, prot):
    '''
        Mutate a nucleotide sequence:

        This script takes a fasta file as input an mutates the sequence according to the insertion, deletion, and mismatches rates.
        Output is a fasta file with the modified entries.

     '''

    if not input_file:
        os.system('genetools mutate --help')
        exit()

    fo = open(input_file+'.M'+str(mutations)+'.m'+str(mismatches)+'.i' +
              str(insertions)+'.d'+str(deletions)+'.prefix-'+prefix+'.mut.fa', 'w')

    # mutations are 2x
    mutations = int(mutations/2)

    # load fasta file
    fasta_file = SeqIO.parse(input_file, 'fasta')
    for record in fasta_file:

        # get the positions to mutate
        _id = record.id
        _sequence = list(record.seq)
        positions = np.array(range(len(_sequence)))
        random.shuffle(positions)
        # print(positions)

        _mutation_rate = int(len(_sequence) * mutations / 100)
        positions_to_mutate = positions[:_mutation_rate]
        random.shuffle(positions_to_mutate)
        # print(positions_to_mutate)

        _mismatches_rate = int(mismatches * _mutation_rate / 100)
        mismatches_positions = positions_to_mutate[:_mismatches_rate]
        # print(mismatches_positions)

        _insertions_rate = int(insertions * _mutation_rate / 100)
        insertions_positions = positions_to_mutate[_mismatches_rate:
                                                   _mismatches_rate + _insertions_rate]
        # print(insertions_positions)

        deletions_positions = positions_to_mutate[_mismatches_rate +
                                                  _insertions_rate:]
        # print(deletions_positions)

        _sequence = mismatch(_sequence, mismatches_positions, prot)
        _sequence = insert(_sequence, insertions_positions,
                           max_indel_size, prot)
        _sequence = delete(_sequence, deletions_positions,
                           max_indel_size, prot)

        entry = "".join(['>mut-', _id, '\n', "".join(_sequence), '\n'])
        fo.write(entry)
