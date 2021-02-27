import os

anno_loc="/csc/mustjoki/gatk/rcc_tumor/rcc_tumor_rna/annovar_g3_org/" #rna
#anno_loc="/csc/mustjoki/gatk/rcc_tumor/rcc_tumor_dna/annovar_g3_org/" #dna
sum=0
for root, dirs, files in os.walk(anno_loc, topdown=True):
	for file in files:
		#print(
		if not file.endswith("hg38_with_annotations.txt") or not "T" in file:
			continue
		os.system("grep '#' /csc/mustjoki/gatk/rcc_tumor/gatk/2426_T_2426_H.somatic2.vcf > /csc/mustjoki2/variant_move/epi_ski/karita/aa_vcf/"+file[:-30]+"_aa_rna_mutations.vcf; tail -n +2 "+root+'/'+file+" | grep -v '[[:space:]]synonymous' | grep 'exonic' | cut -f 196-205 >> /csc/mustjoki2/variant_move/epi_ski/karita/aa_vcf/"+file[:-30]+"_aa_rna_mutations.vcf") 
print(sum)
