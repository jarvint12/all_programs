import subprocess
import os
import re

import mutation_permutation_tool.patient_name as patient_name


def find_sample_id(file):
    pattern=re.compile(r'(HRUH|FHRB)\d\d\d\d?_[A-Z]{2}\d?(_CD\d)?')
    matches=pattern.finditer(file)
    for match in matches:
        return match.group(0)
    else:
        return None



def get_aa_files():
    with open("/csc/mustjoki2/variant_move/epi_ski/pathway_analysis/AA_hMDS_healthy_list_for_Timo.csv", 'r', encoding='utf-8') as f_r:
        lines=f_r.readlines()[1:]
    for root, dirs, files in os.walk('/csc/mustjoki/gatk/aa_genotype/annovar_g3_org/'):
        aa_files=list()
        for file in files:
            if not file.endswith('.vcf') or "NIH" in file or "CLV" in file or "JPN" in file:
                continue
            elif "FHRB1641_BM_CD8" in file or "FHRB1641_BM_CD4" in file:
                aa_files.append(root+'/'+file)
                continue
            #sample_id=find_sample_id(file)
            sample_id=patient_name.main(file)
            if sample_id==None:
                print("SAMPLE_ID NOT FOUND", file)
                continue
            first=True
            for line in lines:
                columns=line.split(',')
                columns[1]=columns[1].strip()
                if ("FHRB1641_BM_CD8" in file and "FHRB1641_BM_CD8" in columns[0]) or ("FHRB1641_BM_CD4" in file and "FHRB1641_BM_CD4" in columns[0]):
                    print(file, columns[0],sample_id in columns[0])
                if sample_id in columns[0]:
                #if columns[0] in sample_id:
                    if columns[1]=="AA":
                        if first:
                            first=False
                        else:
                            print("twice? "+sample_id+", "+columns[0])
                        sample_type="AA"
                        aa_files.append(root+'/'+file)
    return aa_files

def count_mutations(aa_files):
    amount=0
    total=0
    max=("lol", 0)
    min=("CD", 99999999999999)
    nonsynonymous=0
    synonymous=0
    exon_nonsyno=exon_syno=exon_frame=frame=exon_nonframe=nonframe=splicing=0
    for file in aa_files:
        out=subprocess.Popen(["cat "+file+" | grep -v '#' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        mutations=int(stdout.split()[0].decode('utf-8'))
        amount+=1
        total+=mutations #eksonista kaikki, jotka ei ole synonyymisiä, kaikki splicing alueen mutaatiot, paitsi molempiin ehto, että ei saa olla nonframeshift
        if mutations>max[1]:
            max=(file, mutations)
        if mutations<min[1]:
            min=(file, mutations)
        while not os.path.isfile("temp_mutation_load.hg38_multianno.txt"):
            os.system('/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/table_annovar.pl '+file+' \
            /fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/humandb_060418/ -buildver hg38 -otherinfo -remove --vcfinput -protocol refGene -operation g -out temp_mutation_load')

        out=subprocess.Popen(["cat temp_mutation_load.hg38_multianno.txt | grep 'exon' | grep 'nonsynonymous' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        exon_nonsyno+=int(stdout.split()[0].decode('utf-8'))

        out=subprocess.Popen(["cat temp_mutation_load.hg38_multianno.txt | grep 'splicing' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        splicing+=int(stdout.split()[0].decode('utf-8'))

        out=subprocess.Popen(["cat temp_mutation_load.hg38_multianno.txt | grep 'exon' | grep -v 'nonframeshift' | grep 'frameshift' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        exon_frame+=int(stdout.split()[0].decode('utf-8'))

        out=subprocess.Popen(["cat temp_mutation_load.hg38_multianno.txt | grep 'exon' | grep -v 'nonsynonymous' | grep 'synonymous' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        exon_syno+=int(stdout.split()[0].decode('utf-8'))

        out=subprocess.Popen(["cat temp_mutation_load.hg38_multianno.txt | grep 'exon' | grep 'nonframeshift' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        exon_nonframe+=int(stdout.split()[0].decode('utf-8'))

        out=subprocess.Popen(["cat temp_mutation_load.hg38_multianno.txt | grep 'nonsynonymous' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        nonsynonymous+=int(stdout.split()[0].decode('utf-8'))

        out=subprocess.Popen(["cat temp_mutation_load.hg38_multianno.txt | grep -v 'nonframeshift' | grep 'frameshift' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        frame+=int(stdout.split()[0].decode('utf-8'))

        out=subprocess.Popen(["cat temp_mutation_load.hg38_multianno.txt | grep -v 'nonsynonymous' | grep 'synonymous' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        synonymous+=int(stdout.split()[0].decode('utf-8'))

        out=subprocess.Popen(["cat temp_mutation_load.hg38_multianno.txt | grep 'nonframeshift' | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        stdout, stderr=out.communicate()
        nonframe+=int(stdout.split()[0].decode('utf-8'))

        os.system("rm temp_mutation_load*")

    print("Mean variants per sample: "+str(total/amount), "Synonymous:", synonymous/amount, "Nonsynonymous:", nonsynonymous/amount, "Max mutations:", max,"Min mutations:", min, \
    "exon nonsyno:", exon_nonsyno/amount, "exon syno:", exon_syno/amount, "splicing:", splicing/amount, "exon frameshift:", exon_frame/amount, "exon nonframeshift:", exon_nonframe/amount, \
    "Total frameshift:", frame/amount, "Total nonframeshift:", nonframe/amount,)

def main():
    aa_files=get_aa_files()
    print("Amount of AA files: "+str(len(aa_files)))
    count_mutations(aa_files)


if __name__=='__main__':
    main()
