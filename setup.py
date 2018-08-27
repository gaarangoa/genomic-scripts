from setuptools import setup, find_packages

setup(
    name='GeneTools',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'BioPython',
        'ete3',
        'h5py',
        'tqdm'
    ],
    entry_points='''
        [console_scripts]
        genetools=GeneTools.entry:cli
    ''',
)
