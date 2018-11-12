import click
from GeneTools.metastorm.network import network


@click.group()
def metastorm():
    '''
        Tools for processing data from the PATRIC (https://www.patricbrc.org/) database.

        Several scripts to postprocess the data from the PATRIC database.
    '''
    pass


metastorm.add_command(network)
