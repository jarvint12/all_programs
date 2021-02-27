import optparse
import os
import collections
import subprocess
from datetime import datetime
import time

#python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/vcf2muffinn.py -d /csc/mustjoki/gatk/aa_genotype/annovar_g3_org/
#-x /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/muffinn/hs_18499.CCDS.xref --skip "JPN NIH CLV" --destination /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/muffinn/HRUH_muffinn_one/aa/all/
#--prefix aa_all2 --hlist /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/muffinn/AA_hMDS_healthy_list_for_Timo.csv --sample_type AA

#Translates given VCF or annotation files into MUFFINN input(s)

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


def annotate_vcf(values, file):
    line_count=0
    vcf_line_count=get_anno_line_count(file, True)
    while not os.path.isfile(values.destination+'/temp_anno_for_muffinn_'+values.prefix+'.hg38_multianno.txt') or line_count!=vcf_line_count:
        os.system("rm "+values.destination+'/temp_anno_for_muffinn_'+values.prefix+'*')
        os.system(values.table_annovar+' '+file+' \
        '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+values.destination+'/temp_anno_for_muffinn_'+values.prefix)
        time.sleep(1)
        if os.path.isfile(values.destination+'/temp_anno_for_muffinn_'+values.prefix+'.hg38_multianno.txt'):
            line_count=get_anno_line_count(values.destination+'/temp_anno_for_muffinn_'+values.prefix+'.hg38_multianno.txt', False)
    file=values.destination+'/temp_anno_for_muffinn_'+values.prefix+'.hg38_multianno.txt'
    return file


def count_variants(values, f_report):
    files=''
    mutated_genes=collections.Counter()
    print("MUFFINN files: ",values.files)
    for file in values.files:
        if not values.skip_anno:
            file=annotate_vcf(values,file)
        with open(file, 'r') as f_anno:
            next(f_anno)
            for line in f_anno:
                columns=line.replace('\"', '').split()
                if ((columns[5]=="exonic" and columns[8]!="synonymous") or columns[5]=="splicing") and (values.nonframeshift or columns[8]!="nonframeshift"): #If nonsynonymous mutation in exon, or splicing area, and mutation type is not nonframeshift unless it is allowed
                    genes=columns[6].split(',')
                    for gene in genes:
                        mutated_genes[gene]+=1
        if not values.skip_anno:
            os.system("rm "+values.destination+'/temp_anno_for_muffinn_'+values.prefix+'*')
        files=files+file+', '

    with open(values.xref_file, 'r') as f_xref, open(values.destination+'/'+values.prefix+"_MUFFINN_input.txt", 'w+') as f_input:
        found_genes=list()
        for line in f_xref:
            xref_columns=line.split()
            if xref_columns[1] in mutated_genes.keys():
                f_input.write(xref_columns[0]+'\t'+str(mutated_genes[xref_columns[1]])+'\n')
                found_genes.append(xref_columns[1])
        f_input.seek(0)
        found=0
        found_mutations=0
        not_found_genes=0
        ignored_mutations=0
        for gene in mutated_genes:
            if not gene in found_genes:
                f_report.write("Not found: "+gene+', containing '+str(mutated_genes[gene])+' mutations.\n')
                not_found_genes+=1
                ignored_mutations+=mutated_genes[gene]
            else:
                found+=1
                found_mutations+=mutated_genes[gene]
        f_report.write("Found:"+str(found)+" genes and "+str(found_mutations)+" mutations.\nNot found:"+str(not_found_genes)+' genes and '+str(ignored_mutations)+' mutations.\n')
        f_report.write("Input file for file(s) "+files[:-2]+" can be found in file "+values.destination+'/'+values.prefix+"_MUFFINN_input.txt\n")


def go_through_directory(values):
    values.files=list()
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
                if line.split(',')[1]==values.sample_type.strip():
                    filecands.append(line.split(',')[0])
    for root, dirs, files in os.walk(values.directory, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
        for file in files: #Every file in the directory
            if not values.skip_anno:
                if not file.endswith('.vcf'):
                    continue
            else:
                if not file.endswith('hg38_with_annotations.txt'):
                    continue
            in_file_cands=True
            if values.hlist!=None:
                in_file_cands=False
                for cand in filecands:
                    if cand in file or "FHRB1641_BM_CD4" in file or "FHRB1641_BM_CD8" in file:
                        #print(cand)
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
    if values.xref_file==None: #Checks that either file or directory is given
        optparser.error("Give xref file (-x /path/to/file.xref)") #Raises error if not
    if not os.path.isfile(values.xref_file): #If file does not exist
        raise NameError("Could not find file "+values.xref_file+' from directory '+os.getcwd()+'.\n') #Raises error
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
    if not os.path.isdir(values.annovar): #Checks that annovar directory exists
        optparser.error("Could not find directory "+values.annovar+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if not os.path.isfile(values.table_annovar): #Checks that table_annovar.pl exists
        optparser.error("Could not find file "+values.table_annovar+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.prefix==None:
        values.prefix=datetime.now().strftime("%Y%m%dT%H%M%S")
    return values


def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [command] [options]\n\
    Creates input file for muffinn.pl") #Make header for help page
    #Add options to parser

    optparser.add_option("--skip_anno", default=False, action="store_true", dest="skip_anno", help="If your input consists of annovar files")
    optparser.add_option("--nonframeshift", default=False, action="store_true", dest="nonframeshift", help="If you want to count nonframeshift mutations as nonsynonymous")

    group = optparse.OptionGroup(optparser, "Input files options")
    group.add_option("-d", "--directory", dest="directory", help="Directory containing input files if you want to go through whole directory")
    group.add_option("-f", "--file", dest="files", help="If you only have couple of input files (-f /path/to/file)")
    group.add_option("-x", "--xref", dest="xref_file", help="xref file for genes (-x /path/to/file)")
    group.add_option("--filetype", dest="filetype", default='', help="String you want to be in chosen files, for example \"HRUH\"")
    group.add_option("--skip", dest="skip", default='', help="Files you want to be skipped in directory")
    group.add_option("--cd", dest="cd", default='', help="(-cd CD4|CD8|normal) you want to analyze")
    group.add_option("--hlist", dest="hlist", help="List of different types of samples (AA, hMDS, healthy)")
    group.add_option("--sample_type", dest="sample_type", help="AA, hMDS, healthy...")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "Output options")
    group.add_option("--destination", dest="destination", default=os.getcwd(), help="destination to cdf file, report etc. (--destination /path/to/directory). Default is current directory")
    group.add_option("--prefix", dest="prefix", help="Prefix for output-files, default is timestamp")
    group.add_option("--multiple_output", default=False, action="store_true", dest="multiple", help="If you want own output file for every input file")
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
    report=values.destination+'/'+values.prefix+"_MUFFINN_vcf2muffinn_report.txt"
    f_report= open(report, 'w+')
    if values.multiple and len(values.files)>1:
        files=values.files
        i=0
        prefix_orig=values.prefix
        for file in files:
            values.files=[file]
            values.prefix=prefix_orig+'_'+str(i)
            count_variants(values, f_report)
            i+=1
    else:
        count_variants(values, f_report)
    f_report.close()


if __name__=='__main__':
    main()

    #found: 9469 Not found: 4422
 #OUTPUT 1 0 1 /fs/vault/pipelines/gatk/data/MutSigCV.1.4/hg38_ens/GCF_000001405.37_GRCh38.p11_assembly_report.txt /csc/mustjoki2/variant_move/epi_ski/annovar_org/181019_A00464_0029_BH7MCLDSXX_Epi-Ski_824_S119_L001.trimmed.final.somatic.artifact.repon.repon.vcf.hg38_annotation_filtered.txt 0
