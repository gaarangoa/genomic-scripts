import click
from GeneTools.mutate import mutate
from GeneTools.patric.patric import patric
from GeneTools.metastorm.metastorm import metastorm
from GeneTools.fasta2rand import fasta2rand
from GeneTools.FilterFastaLength import FilterFastaLength
from GeneTools.filterTaxa import filter_taxa
from GeneTools.filter_fastq import filter_fastq
from GeneTools.taxa_file_to_table import taxa_file_to_table
from GeneTools.deeparg_table import deeparg_table
from GeneTools.deeparg_abundance import deeparg_abundance
from GeneTools.fasta_subset import fasta_subset
from GeneTools.split_fasta import split_fasta
from GeneTools.fasta2kmers import fasta2kmers
from GeneTools.fasta2trainKmers import fasta2trainKmers
from GeneTools.fasta_filter_seq import fasta_filter_seq
from GeneTools.fasta2len import fasta2len


@click.group()
def cli():
    '''
        Gene Tools:  Is a suit of scripts useful for the manipulation of NGS and genomics data.

        Author(s):   Gustavo Arango (gustavo1@vt.edu)

        Usage:       genetools --help
    '''
    pass


cli.add_command(mutate)
cli.add_command(patric)
cli.add_command(fasta2rand)
cli.add_command(FilterFastaLength)
cli.add_command(filter_taxa)
cli.add_command(filter_fastq)
cli.add_command(taxa_file_to_table)
cli.add_command(deeparg_table)
cli.add_command(deeparg_abundance)
cli.add_command(fasta_subset)
cli.add_command(split_fasta)
cli.add_command(fasta2kmers)
cli.add_command(fasta_filter_seq)
cli.add_command(fasta2trainKmers)
cli.add_command(fasta2len)
cli.add_command(metastorm)
