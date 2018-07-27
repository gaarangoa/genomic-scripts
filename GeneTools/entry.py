import click
from GeneTools.mutate import mutate

@click.group()
def cli():
    '''
        Gene Tools:  Is a suit of scripts useful for the manipulation of NGS and genomics data.

        Author(s):   Gustavo Arango (gustavo1@vt.edu)

        Usage:       genetools --help
    '''
    pass


cli.add_command(mutate)
