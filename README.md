## GENETOOLS

This repository contains a collection of commonly used wrappers/scripts/preprocessing scripts for the genomic/metagenomic analysis.

## SETUP
Download this repository and install it using pip3

	git clone https://github.com/gaarangoa/genomic-scripts.git
	cd genomic-scripts
	pip3 install . --user

## USAGE

	genetools --help
	Usage: genetools [OPTIONS] COMMAND [ARGS]...
	Gene Tools:  Is a suit of scripts useful for the manipulation of NGS and genomics data.
	Author(s): Gustavo Arango (gustavo1@vt.edu)

	Usage: genetools --help

	Options:
		--help  Show this message and exit.
	Commands:
		mutate  Mutate a nucleotide sequence:


<!-- ### Fasq to Fasta
this simple script takes a fasta file as input and retorns a fasta file

	fq2fa.py input.fq{fastq}

### Split Fastq
this simple script splits fastq files that are stored in one single fastq file. It looks at the prefix (you need to define where the 1/2 field) and store them into different files

	fqsplit.py input.fq{fastq}

## fasta to length
This script calculates the length of each entry in a fasta file and store it as a text file

	fasta2len.py input_file "..." > output_file

"..." is the separator of each entry name (if needed)

## get random sequences from fastq file
This script takes a paired end library and subsample the sequences to a user defined number. Please make sure the seed parameter is the same for both paired-1 and paired-2, other case you will end up having different reads in each one of the subsampled files.

### Requirements
This script uses vsearch (https://github.com/torognes/vsearch). There is a local copy of vsearch in this repository, but only works in linux systems. To use it, you need to type:

	chmod +x vsearch

### Usage
To use the randomfq.sh script, you need to be in the directory where the file was downloaded, then, you just need to type:

	sh randomfq.sh fastq_file_1 fastq_file_2 number_of_reads seed


# Use Cases
## Remove chloroplast reads

In this use case we will remove the chloroplasts from a sample and then subsample the library to 12M reads.

First we need to create a virtual environment where we can download our software:

	virtualenv env
	source ./env/bin/activate

now we need to install the software to remove the chloroplasts from the library, we will use chfilter.

	pip install pip --upgrade
	pip install chfilter

then we need to clone this repository

	git clone https://github.com/gaarangoa/genomic-scripts.git

I am assuming the directory root to be like this:

	----| root
		+---| rawreads
		+---+--| sample_1
		+---| genomic-scripts

### Remove 16S rRNA chloroplast reads from sample and random subsample.

For this task we will use Chfilter, which assumes that you have already installed bowtie 2 in your machine, so it can be used by just typing bowtie2

1. uncompress *.gz files

		cd rawreads/sample_1/
		gunzip sample_1.R1.fastq.gz
		gunzip sample_2.R2.fastq.gz

2. Run chfilter to remove chloroplasts

		chfilter remove --paired-1 sample_1.R1.fastq --paired-2 sample_1.R2.fastq --out-dir .

3. Subsample 12M reads from the sample without chloroplast 16S reads. If you subsample one library multiple times, make sure to change the random seed, othercase you will get the same result. In this example we set the random seed to 0.

		cd ../../genomic-scripts/
		sh randomfq.sh sample_1.R1.no-chl.fastq sample_1.R2.no-chl.fastq 12700000 0
		gzip *.fq

4. Analysis can be done in MetaStorm (http://bench.cs.vt.edu/MetaStorm/) -->

