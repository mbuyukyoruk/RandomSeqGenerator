from random import choice, shuffle, uniform
import argparse
import sys
import re
import time
import textwrap

orig_stdout = sys.stdout

try:
    import tqdm
except:
    print("tqdm module is not installed! Please install tqdm and try again.")
    sys.exit()

parser = argparse.ArgumentParser(prog='python RandomSeqGenerator.py',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''\

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
	-n/--num		    number			Specify number of sequences to generate.

	-l/--len		    length			Specify number of sequences to generate.

	-gcf/--gc_fix		All GC%	        Specify desired gc content for all sequences (i.e., 0.5).

	-gcr/--gc_range		All GC%	        Specify desired gc content range (i.e., 0.4-0.5).

	-t/--type           Type            DNA or RNA.

Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.

      	'''))
parser.add_argument('-n', '--num', required=True, type=int, dest='num',
                    help='Specify number of sequences to generate.\n')
parser.add_argument('-l', '--len', required=True, type=int, dest='seq_len',
                    help='Specify number of sequences to generate.\n')
parser.add_argument('-gcf', '--gc_fix', required=False, type=float, dest='gc_f', default=0.5,
                    help='Specify desired gc content for all sequences (i.e., 0.5).\n')
parser.add_argument('-gcr', '--gc_range', required=False, type=str, dest='gc_r',
                    help='Specify desired gc content range (i.e., 0.4-0.5).\n')
parser.add_argument('-t', '--type', required=False, type=str, dest='seq_type', default="DNA",
                    help='DNA or RNA.\n')

results = parser.parse_args()
num = results.num
seq_len = results.seq_len
gc_f = results.gc_f
gc_r = results.gc_r
seq_type = results.seq_type

if seq_type.lower() not in ["dna", "rna"]:
    print("Supports only DNA or RNA!")
    sys.exit()
else:
    pass

timestr = time.strftime("%Y%m%d_%H%M%S")


def generate_dna(length, required, percent):
    n = int(round(percent * length))
    if seq_type.lower() == "dna":
        fillin = list(set('GCTA') - set(required))
    else:
        fillin = list(set('GCUA') - set(required))
    dna = [choice(required) for _ in range(n)]
    dna += [choice(fillin) for _ in range(length - n)]
    shuffle(dna)
    return ''.join(dna)


generated = set()

with tqdm.tqdm(range(num)) as pbar:
    pbar.set_description('Generating...')
    while len(generated) < num:
        pbar.update()
        if gc_r != None:
            low = float(gc_r.split("-")[0])
            high = float(gc_r.split("-")[1])
            gc = uniform(low, high)
        else:
            gc = gc_f

        generated.add(generate_dna(seq_len, 'GC', gc))
result = list(generated)

with tqdm.tqdm(range(len(result))) as pbar:
    pbar.set_description('Writing...')
    for i in range(len(result)):
        pbar.update()
        A = float(result[i].count("A"))
        if seq_type.lower() == "dna":
            T = float(result[i].count("T"))
        else:
            T = float(result[i].count("U"))
        G = float(result[i].count("G"))
        C = float(result[i].count("C"))
        f = open("Random_" + str(seq_len) + "bp_seq_" + timestr + ".fasta", 'a')
        sys.stdout = f
        print('>Random_seq_' + str(i + 1) + " | " + str((G + C) / (A + T + G + C) * 100) + "% GC content | A:" + str(
            int(A)) + " T(U):" + str(int(T)) + " G:" + str(int(G)) + " C:" + str(int(C)))
        print(re.sub("(.{60})", "\\1\n", result[i], 0, re.DOTALL))
