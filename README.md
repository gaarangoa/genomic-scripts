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

	fasta2len.py input_file "..." > output file

"..." is the separator of each entry name (if needed)
