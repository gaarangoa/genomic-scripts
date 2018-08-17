import click
from GeneTools.mutate import mutate
from GeneTools.patric.patric import patric
from GeneTools.fasta2rand import fasta2rand
from GeneTools.FilterFastaLength import FilterFastaLength

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
