import optparse
import os
import collections
import subprocess
from datetime import datetime
import time


#python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/fusiate_onco_input.py -d /csc/mustjoki/gatk/aa_genotype/annovar_g3_org/
#--skip "JPN NIH CLV" --destination /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/oncodrivefm/HRUH_one/aa/all/
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
    while not os.path.isfile(values.destination+'/temp_anno_for_onco_'+values.prefix+'.hg38_multianno.txt') or line_count!=vcf_line_count:
        os.system("rm "+values.destination+'/temp_anno_for_onco_'+values.prefix+'.*')
        os.system(values.table_annovar+' '+file+' \
        '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+values.destination+'/temp_anno_for_onco_'+values.prefix)
        print(values.table_annovar+' '+file+' \
        '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+values.destination+'/temp_anno_for_onco_'+values.prefix)
        time.sleep(1)
        if os.path.isfile(values.destination+'/temp_anno_for_onco_'+values.prefix+'.hg38_multianno.txt'):
            line_count=get_anno_line_count(values.destination+'/temp_anno_for_onco_'+values.prefix+'.hg38_multianno.txt', False)
    file=values.destination+'/temp_anno_for_onco_'+values.prefix+'.hg38_multianno.txt'
    return file


def create_inputs(values):
    report=values.destination+'/'+values.prefix+"_fusiate_onco_report.txt"
    f_report= open(report, 'w+')
    currentDT=datetime.now()
    if values.multiple:
        i=0
        prefix_orig=values.prefix
        for file in values.files:
            if values.annotate_input:
                file=annotate_input(values, file)
            if len(values.files)>1:
                values.prefix=prefix_orig+'_'+str(i)
            while not (os.path.isfile(values.destination+'/temp_fusiate_'+values.prefix+'.oncordive.txt')):
                os.system('perl /fs/vault/pipelines/gatk/src/1.0/annovar2oncodrive.pm '+values.destination+'/'+values.prefix+ \
                ' 1 0 0 0 /fs/vault/pipelines/gatk/data/MutSigCV.1.4/hg38_ens/GCF_000001405.37_GRCh38.p11_assembly_report.txt '+file+' 0')
                print('perl /fs/vault/pipelines/gatk/src/1.0/annovar2oncodrive.pm '+values.destination+'/'+values.prefix+ \
                ' 1 0 0 0 /fs/vault/pipelines/gatk/data/MutSigCV.1.4/hg38_ens/GCF_000001405.37_GRCh38.p11_assembly_report.txt '+file+' 0')
            f_report.write("File "+file+" input was stored in file "+values.destination+'/values.prefix\n')
            if values.annotate_input:
                os.system("rm "+values.destination+'/temp_anno_for_onco_'+values.prefix+'.*')
            i+=1
    else:
        onco_file=values.destination+'/'+values.prefix+"_oncodrive.txt"
        print("Oncodrive files: ",values.files)
        f_onco= open(onco_file, 'w+')
        for file in values.files:
            if values.annotate_input:
                file=annotate_input(values, file)
            while not (os.path.isfile(values.destination+'/temp_fusiate_'+values.prefix+'.oncordive.txt')):
                os.system('perl /fs/vault/pipelines/gatk/src/1.0/annovar2oncodrive.pm '+values.destination+'/temp_fusiate_'+values.prefix+' 1 0 0 0 \
                /fs/vault/pipelines/gatk/data/MutSigCV.1.4/hg38_ens/GCF_000001405.37_GRCh38.p11_assembly_report.txt '+file+' 0')
            with open(values.destination+'/temp_fusiate_'+values.prefix+'.oncordive.txt', 'r') as f_temp:
                for line in f_temp:
                    f_onco.write(line)
            f_report.write(file+'\n')
            os.system("rm "+values.destination+'/temp_fusiate_'+values.prefix+'.*')
            os.system("rm "+values.destination+'/temp_fusiate_'+values.prefix+'_*')
            if values.annotate_input and not values.keep_anno:
                os.system("rm "+values.destination+'/temp_anno_for_onco_'+values.prefix+'.*')
        f_onco.close()


def submit_shells(values):
    i=0
    for file in values.files:
        os.system("grun.py -n onc_"+str(i)+" -q all.q -c \"source /homes/tijarvin/anaconda3/bin/activate tpyenv; python3 "+
        "/csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/fusiate_onco_input.py "+
        "--file "+file+" --destination "+values.destination+" --prefix "+values.prefix+"_"+str(i)+" --annotate_input --keep_anno\"")
        i+=1


def go_through_directory(values):
    #print("values:",values.cd, values.sample_type, values.destination)
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
    Creates input file for oncodrive-fm") #Make header for help page
    #Add options to parser

    optparser.add_option("--separate_runs", default=False, action="store_true", help="If you want to create input files for onco, separately.")

    group = optparse.OptionGroup(optparser, "Input files options")
    group.add_option("-f", "--file", dest="files", help="File for Oncodrive (-f /path/to/file)")
    group.add_option("-d", "--directory", dest="directory", help="Directory containing files")
    group.add_option("--annotate_input", dest="annotate_input", action="store_true", default=False, help="If your input is not yet annotated (VCF files). Default: %default")
    group.add_option("--filetype", dest="filetype", default='', help="String you want to be in chosen files, for example \"HRUH\"")
    group.add_option("--skip", dest="skip", help="Files you want to be skipped in directory")
    group.add_option("--hlist", dest="hlist", help="List of different types of samples (AA, hMDS, healthy)")
    group.add_option("--sample_type", dest="sample_type", help="AA, hMDS, healthy...")
    group.add_option("--cd", dest="cd", default='', help="(-cd CD4|CD8|normal) you want to analyze")
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
    group.add_option("--keep_anno", default=False, action="store_true", dest="keep_anno", help="If you don't want to remove annotated files")
    optparser.add_option_group(group)

    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    return check_optparsing(values, optparser)


def main():
    values=optparsing()
    if values.separate_runs:
        submit_shells(values)
    else:
        create_inputs(values)



if __name__=='__main__':
    main()
