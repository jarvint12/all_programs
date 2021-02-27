import optparse
import os
import collections
import subprocess
from datetime import datetime
import time


#python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/dendrix_multiple_input.py -d /csc/mustjoki/gatk/aa_genotype/annovar_g3_org/
#--skip "JPN NIH CLV" --destination /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/dendrix/HRUH/aa/all/
#--prefix aa_all2 --hlist /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/muffinn/AA_hMDS_healthy_list_for_Timo.csv --sample_type AA --annotate_input



def get_anno_line_count(file, is_vcf):
    if is_vcf:
        p = subprocess.Popen('cat '+file+' | grep -v "#" | wc -l', shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
        out, err = p.communicate()
        return int(out.decode().strip())+1 #header
    else:
        p = subprocess.Popen('cat '+file+' | wc -l', shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
        out, err = p.communicate()
        return int(out.decode().strip())


def annotate_input(values, file):
    line_count=0
    vcf_line_count=get_anno_line_count(file, True)
    while not os.path.isfile(values.destination+'/temp_anno_for_dendrix_'+values.prefix+'.hg38_multianno.txt') or line_count!=vcf_line_count:
        os.system("rm "+values.destination+'/temp_anno_for_onco_'+values.prefix+'*')
        os.system(values.table_annovar+' '+file+' \
        '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+values.destination+'/temp_anno_for_dendrix_'+values.prefix)
        time.sleep(1)
        if os.path.isfile(values.destination+'/temp_anno_for_dendrix_'+values.prefix+'.hg38_multianno.txt'):
            line_count=get_anno_line_count(values.destination+'/temp_anno_for_dendrix_'+values.prefix+'.hg38_multianno.txt', False)
    file=values.destination+'/temp_anno_for_dendrix_'+values.prefix+'.hg38_multianno.txt'
    return file



def analyzed_files(values, gene_file, pathway_file):
    #print("GEENIJUTTU",gene_file)
    with open(gene_file, 'r') as fg_r:
        genes=list()
        for line in fg_r:
            columns=line.split()
            columns=columns[1:]
        for gene in columns:
            if not gene in genes:
                genes.append(gene)
    with open(values.destination+'/'+values.prefix+'_analyzed_genes.txt', 'w+') as fg_w:
        for gene in genes:
            fg_w.write(gene+'\n')
    with open(pathway_file, 'r') as fp_r:
        pathways=list()
        for line in fp_r:
            columns=line.split()
            columns=columns[1:]
            for pathway in columns:
                if not pathway in pathways:
                    pathways.append(pathway)
    with open(values.destination+'/'+values.prefix+'_analyzed_pathways.txt', 'w+') as fp_w:
        for pathway in pathways:
            fp_w.write(pathway+'\n')


def multiple_outputs(values, f_report):
    i=0
    prefix_orig=values.prefix
    for file in values.files:
        if values.annotate_input:
            file=annotate_input(values, file)
        if len(files)>1:
            values.prefix=prefix_orig+'_'+str(i)
        while not os.path.isfile(values.destination+'/'+values.prefix+'.dendrix.pathway.txt') or not os.path.isfile(values.destination+'/'+values.prefix+'.dendrix.gene.txt'):
            os.system('perl /fs/vault/pipelines/gatk/src/1.0/annovar2oncodrive.pm '+values.destination+'/'+values.prefix+ \
            ' 1 0 0 1 /fs/vault/pipelines/gatk/data/MutSigCV.1.4/hg38_ens/GCF_000001405.37_GRCh38.p11_assembly_report.txt '+file+' 0')
            time.sleep(1)
        f_report.write("File "+file+" input was stored in file "+values.destination+'/'+values.prefix+'\n')
        os.system("rm "+values.destination+'/'+values.prefix+'.oncordive.txt')
        if values.annotate_input:
            os.system("rm "+values.destination+'/temp_anno_for_dendrix_'+values.prefix+'*')
        time.sleep(1)
        analyzed_files(values, values.destination+'/'+values.prefix+'.dendrix.gene.txt', values.destination+'/'+values.prefix+'.dendrix.pathway.txt')
        i+=1


def combinated_output(values, f_report):
    input_file_gene=values.destination+'/'+values.prefix+"_dendrix_multiple_input.gene.txt"
    f_input_gene= open(input_file_gene, 'w+')
    input_file=values.destination+'/'+values.prefix+"_dendrix_multiple_input.pathway.txt"
    f_input= open(input_file, 'w+')
    print("Dendrix files: ",values.files)
    for file in values.files:
        if values.annotate_input:
            file=annotate_input(values, file)
        while not os.path.isfile(values.destination+'/temp_fusiate_'+values.prefix+'.dendrix.pathway.txt') or not os.path.isfile(values.destination+'/temp_fusiate_'+values.prefix+'.dendrix.gene.txt'):
            os.system('perl /fs/vault/pipelines/gatk/src/1.0/annovar2oncodrive.pm '+values.destination+'/temp_fusiate_'+values.prefix+' 1 0 0 1 \
            /fs/vault/pipelines/gatk/data/MutSigCV.1.4/hg38_ens/GCF_000001405.37_GRCh38.p11_assembly_report.txt '+file+' 0')
            time.sleep(1)
        with open(values.destination+'/temp_fusiate_'+values.prefix+'.dendrix.pathway.txt', 'r') as f_temp:
            for line in f_temp:
                f_input.write(line)
        with open(values.destination+'/temp_fusiate_'+values.prefix+'.dendrix.gene.txt', 'r') as f_temp:
            for line in f_temp:
                f_input_gene.write(line)
        f_report.write(file+'\n')
        os.system("rm "+values.destination+'/temp_fusiate_'+values.prefix+'.*')
        os.system("rm "+values.destination+'/temp_fusiate_'+values.prefix+'_*')
        if values.annotate_input:
            os.system("rm "+values.destination+'/temp_anno_for_dendrix_'+values.prefix+'*')
        time.sleep(1)
    f_input.close()
    f_input_gene.close()
    return input_file_gene, input_file


def go_through_directory(values):
    values.files=list()
    #print(values.cd, values.sample_type)
    if values.filetype!='':
        words=values.filetype.split()
    else:
        words=['']
    if values.skip!=None:
        skip=values.skip.split()
    if values.hlist!=None:
        filecands=list()
        with open(values.hlist, encoding='utf-8') as f:
            for line in f.readlines():
                line=line.strip()
                #print(line)
                if line.split(',')[1]==values.sample_type.strip():
                    filecands.append(line.split(',')[0])
    for root, dirs, files in os.walk(values.directory, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
        for file in files: #Every file in the directory
            if values.annotate_input and not file.endswith('.vcf'):
                continue
            elif not values.annotate_input and not file.endswith('hg38_with_annotations.txt'):
                continue
            in_file_cands=True
            if values.hlist!=None:
                in_file_cands=False
                for cand in filecands:
                    if cand in file or "FHRB1641_BM_CD4" in file or "FHRB1641_BM_CD8" in file:
                        in_file_cands=True
            if not in_file_cands:
                continue
            wanted=True
            if values.skip!=None:
                for string in skip:
                    if string in file:
                        wanted=False
            if not wanted:
                continue
            for word in words:
                if word in file:
                    if values.cd in file:
                        values.files.append(root+'/'+file)
                        print(root+'/'+file)
                        break
    return values

def check_optparsing(values, optparser):
    if values.files==None and values.directory==None: #Checks that either file or directory is given
        optparser.error("Give file (-f /path/to/file) or directory (-d /path/to/directory)") #Raises error if not
    if values.files!=None: #If file does not exist
        values.files=values.files.split()
        for file in values.files:
            if not os.path.isfile(file):
                raise NameError("Could not find file "+file+' from directory '+os.getcwd()+'.\n') #Raises error
    if not os.path.isdir(values.destination): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.destination+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.hlist!=None:
        if values.sample_type==None:
            optparser.error("Give sample type you want to include (AA, hMDS, healthy).\n")
        if not os.path.isfile(values.hlist):
            raise NameError("Could not find file "+values.hlist+' from directory '+os.getcwd()+'.\n') #Raises error
        if values.directory==None: #Checks that either file or directory is given
            optparser.error("Give directory (-d /path/to/directory)") #Raises error if not
    if values.directory!=None:
        if not os.path.isdir(values.directory): #Checks that destination directory exists
            optparser.error("Could not find directory "+values.directory+' from directory '+os.getcwd()+'.\n') #Directory was not found
        values = go_through_directory(values)
    if values.prefix==None:
        values.prefix=datetime.now().strftime("%Y%m%dT%H%M%S")
    return values


def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [command] [options]\n\
    Creates input file for muffinn.pl") #Make header for help page
    #Add options to parser

    group = optparse.OptionGroup(optparser, "Input files options")
    group.add_option("-f", "--file", dest="files", help="File for MUFFINN (-f /path/to/file)")
    group.add_option("-d", "--directory", dest="directory", help="Directory containing files")
    group.add_option("--annotate_input", dest="annotate_input", action="store_true", default=False, help="If your input is not yet annotated (VCF files). Default: %default")
    group.add_option("--filetype", dest="filetype", default='', help="Files you want to be added in directory")
    group.add_option("--skip", dest="skip", help="Files you want to be skipped in directory")
    group.add_option("--hlist", dest="hlist", help="List of different types of samples (AA, hMDS, healthy)")
    group.add_option("--sample_type", dest="sample_type", help="AA, hMDS, healthy...")
    group.add_option("--cd", dest="cd", default='', help="(-cd CD4|CD8|normal) you want to analyze")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "Output options")
    optparser.add_option("--destination", dest="destination", default=os.getcwd(), help="destination to cdf file, report etc. (--destination /path/to/directory). Default is current directory")
    optparser.add_option("--prefix", dest="prefix", help="Prefix for output-files, default: %default")
    optparser.add_option("--multiple_output", default=False, action="store_true", dest="multiple", help="If you want own output file for every input file")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "ANNOVAR options")
    group.add_option("--annovar", dest="annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/humandb_060418/', help="Location of annovar, default=/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/humandb_060418/'")
    group.add_option("--buildver", dest="buildver", default='hg38', help="Buildver version, default=hg38")
    group.add_option("--table_annovar", dest="table_annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/table_annovar.pl', help="Location of table_annovar.pl, default=/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/table_annovar.pl")
    optparser.add_option_group(group)

    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    return check_optparsing(values, optparser)


def main():
    values=optparsing()
    report=values.destination+'/'+values.prefix+"_dendrix_multiple_input_report.txt"

    f_report= open(report, 'w+')

    if values.multiple:
        multiple_outputs(values, f_report)
    else:
        gene_file, pathway_file = combinated_output(values,f_report)
        analyzed_files(values, gene_file, pathway_file)
    f_report.close()



if __name__=='__main__':
    main()
