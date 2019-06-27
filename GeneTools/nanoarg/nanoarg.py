import click
from GeneTools.nanoarg.mapping_table import mapping_table
from GeneTools.nanoarg.network import network


@click.group()
def nanoarg():
    '''

        Tools for processing the JSON file from nanoARG.

    '''
    pass


nanoarg.add_command(mapping_table)
nanoarg.add_command(network)
