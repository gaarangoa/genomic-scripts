import click
from GeneTools.mutate import mutate
from GeneTools.patric.patric import patric
from GeneTools.fasta2rand import fasta2rand
from GeneTools.FilterFastaLength import FilterFastaLength
from GeneTools.filterTaxa import filter_taxa
from GeneTools.filter_fastq import filter_fastq
from GeneTools.taxa_file_to_table import taxa_file_to_table
from GeneTools.deeparg_table import deeparg_table

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
