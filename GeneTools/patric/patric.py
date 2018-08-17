import click
from GeneTools.patric.subtract_genes import subtract_genes


@click.group()
def patric():
    '''
        Tools for processing data from the PATRIC (https://www.patricbrc.org/) database.

        Several scripts to postprocess the data from the PATRIC database.
    '''
    pass


patric.add_command(subtract_genes)
