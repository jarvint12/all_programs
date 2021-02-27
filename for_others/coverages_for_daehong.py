import subprocess
import os


p=subprocess.Popen('find /csc/mustjoki/gatk/rna_cont_analysis/htlv -name \'*.dedub.bam.left.nonsplit.bam\' 2>&1 | grep -v \'CD4\' | grep -v \'HTLV60011_PB_CD8\' | grep -v \'HTLV60377_PB_CD8\' | grep -v \"Permission denied\"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
files=out.decode().split('\n')
number_of_files=0
string="--destination /csc/mustjoki2/variant_move/epi_ski/daehong/immuno_crop/ --bed_file /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/immunopanel_genes.bed --skip_permutation --no_vcf_generate -b \'"
for file in files[:-1]: #Last parameter is string
	string+=file+' '
	number_of_files+=1
print(number_of_files)
string=string[:-1]+"\'" #remove last space
os.system("grun.py -n coverages_plots -q all.q -c \"source /homes/tijarvin/anaconda3/bin/activate tpyenv; python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/mutation_permutation_tool/mutation_load3.py "+string+"\"")
