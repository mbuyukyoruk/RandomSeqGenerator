# RandomSeqGenerator

Author: Murat Buyukyoruk

        RandomSeqGenerator help:

This script is developed to fetch sequences from multifasta file by using a list of accession numbers to fetch. 

SeqIO package from Bio is required to fetch sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.

Syntax:

        python RandomSeqGenerator.py -n 100 -l 500 -gcr 0.5-0.7 -t DNA

RandomSeqGenerator dependencies:

tqdm                                                refer to https://pypi.org/project/tqdm/

Input Paramaters (REQUIRED):
----------------------------
	-n/--num		number		Specify number of sequences to generate.

	-l/--len		length		Specify number of sequences to generate.

	-gcf/--gc_fix		All GC%	        Specify desired gc content for all sequences (i.e., 0.5).

	-gcr/--gc_range		All GC%	        Specify desired gc content range (i.e., 0.4-0.5).

	-t/--type		Type            DNA or RNA.

Basic Options:
--------------
	-h/--help		HELP		Shows this help text and exits the run.

