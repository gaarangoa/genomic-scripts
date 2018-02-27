fq_1=$1
fq_2=$2
reads=$3
seed=$4

# subsample fastq 1
./vsearch --fastx_subsample $fq_1 --fastqout $fq_1.sub.$reads.fq  --sample_size $reads --randseed $seed

# subsample fastq 2
./vsearch --fastx_subsample $fq_2 --fastqout $fq_2.sub.$reads.fq  --sample_size $reads --randseed $seed

