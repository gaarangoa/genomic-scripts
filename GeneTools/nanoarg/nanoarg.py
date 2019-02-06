import click
from GeneTools.nanoarg.mapping_table import mapping_table


@click.group()
def nanoarg():
    '''

        Tools for processing the JSON file from nanoARG.

    '''
    pass


nanoarg.add_command(mapping_table)
