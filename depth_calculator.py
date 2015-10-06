#!/usr/bin/env python

helptext='''This script will use bwa and samtools to determine the depth of coverage 
across a sequence generated by HybSeqPipeline. Reads will be mapped against the coding
sequence. The coding sequence will be aligned to the reference gene, and depth estimates
will be relative to the reference.

By default the script will do this for the CDS generated for the gene.
If you have run the "get_introns.py" script on the gene, you can get coverage for those
regions instead with --introns

'''

import sys,os,argparse,shutil
from Bio import SeqIO


def merge_seqs(genelist,prefix):
	'''Given a list of gene sequences, retreive the sequences and generate a single FASTA file.'''
	with open("coding_sequences.fasta","w") as outfile:
		for gene in genelist:
			SeqIO.write(SeqIO.read("{}/{}/sequences/FNA/{}.FNA".format(gene,prefix,gene),'fasta'),outfile,'fasta')

def build_index():
	bwa_index_cmd = "bwa index coding_sequences.fasta"
	os.system(bwa_index_cmd)	


def pileup_cds():
	bwa_index_cmd = "bwa index {}/sequences/FNA/{}.FNA".format(prefix,gene_name)
	bwa_samtools_cmd = "bwa mem -t {} {} ../../{}* | samtools view -bS - | samtools sort - cds.sorted".format(cpus,bwa_index_loc,reads_stem)
	pileup_cmd = "samtools mpileup cds.sorted.bam"


def main():
	parser = argparse.ArgumentParser(description=helptext,formatter_class=argparse.RawTextHelpFormatter)
	#parser.add_argument("--introns",help="Calculate coverage from all exonerate contigs, not just surviving coding sequence.",default=False,action=store_true)
	#parser.add_argument("-c","--cds_fn",help="Fasta file of coding domain sequences (nucleotides), should have same names as corresponding protein file.",default=None)
	parser.add_argument("--genelist",help="Optional list of genes to retreive coverage. Default is to use genes_with_seqs.txt")

	parser.add_argument("-r","--reads",help="FastQ read file(s) for mapping to the sequence.",nargs='+',required=True)
	parser.add_argument("--prefix",help="Prefix of sample directory generated by HybSeqPipeline",required=True)
	
	args=parser.parse_args()
	
	if len(sys.argv) < 2:
		print helptext
		sys.exit(1)

	if os.path.isdir(args.prefix):
		os.chdir(args.prefix)
	else:	
		sys.stderr.write("Directory {} not found!\n".format(args.prefix))
		sys.exit(1)	
		
	if args.genelist:
		genelist = [x.rstrip() for x in open(args.genelist).readlines()]
	else:
		genelist = [x.split()[0] for x in open('genes_with_seqs.txt').readlines()]
	
	merge_seqs(genelist,args.prefix)
	build_index()				



if __name__ == '__main__': main()
