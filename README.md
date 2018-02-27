## USEFUL SCRIPTS
This repository contains a collection of commonly used wrappers/scripts/preprocessing scripts for the genomic/metagenomic analysis.

### Fasq to Fasta
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
