import optparse
import os
import collections
import subprocess
from datetime import datetime
import re

import patient_name

## Go through aplastic anemia data and chooses given type of bam files for mutation load tool

def make_shell_file(values, bam_command, vcf_command,prefix):
    if not os.path.isdir(values.destination+'/'+prefix):
        os.mkdir(values.destination+'/'+prefix)
    print("grun.py -n "+prefix+" -q hugemem.q -c \"source /homes/tijarvin/anaconda3/bin/activate tpyenv; " + \
    "python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/mutation_permutation_tool/mutation_load3.py --vcf_file \\\" "+
    vcf_command+"\\\" -b \\\""+bam_command+"\\\" --destination "+values.destination+'/'+prefix+" --separate_syn --intergenic --perm_amount 100\"")
    os.system("grun.py -n "+prefix+" -q hugemem.q -c \"source /homes/tijarvin/anaconda3/bin/activate tpyenv; " + \
    "python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/mutation_permutation_tool/mutation_load3.py --vcf_file \\\" "+
    vcf_command+"\\\" -b \\\""+bam_command+"\\\" --destination "+values.destination+'/'+prefix+" --separate_syn --intergenic --perm_amount 100 --prefix "+prefix+"\"")

    #with open(values.destination+'/permutation_'prefix+'.sh', 'w+') as f_p:
#        f_p.write("#$ -N Permutation_HRUH_"+str(i)+"\n#$ -q hugemem.q\n#$ -cwd\n#$ -e /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/qsub_output/permutation_"+prefix+"_e.txt\n")
#        f_p.write("#$ -o /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/qsub_output/permutation_HRUH_"+str(i)+"_o.txt\nsource /homes/tijarvin/anaconda3/bin/activate tpyenv\n")
#        f_p.write("python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/mutation_permutation_tool/mutation_load3.py --vcf_file \""+
#        vcf_command+"\" -b \""+bam_command+"\" --destination /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/"+str(i)+"/ ")
#        f_p.write("--separate_syn --intergenic --perm_amount 100")
#    return values.destination+'/permutation_HRUH_'+str(i)+'.sh'

def make_parameters(values):
    bam_files=''
    vcf_command=''
    tot_bams=0
    tot_vcf=0
    i=0
    list_of_bams=values.files
    for bam_file in list_of_bams:
        #if not "FHRB1641" in bam_file or "10-15" in bam_file:
        #    continue
        bam_files=bam_files+' '+bam_file
        tot_bams+=1
        filename=patient_name.main(bam_file.strip())
        if values.only_sampleid:
            print(filename, bam_file)
            continue
        found=False
        for root, dirs, files in os.walk(values.vcf_location, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
            for vcf_file in files: #Every file in the directory
                if not vcf_file.endswith("norm.vcf"):
                    continue
                if filename==None:
                    print(bam_file)
                if filename in vcf_file:
                    vcf_command=vcf_command+' '+root+'/'+vcf_file
                    tot_vcf+=1
                    found=True
                    break
            if found:
                break
        if tot_bams%values.batch_size==0 and not values.only_count:
            make_shell_file(values, bam_files, vcf_command,values.prefix+"_"+str(i))
            i+=1
            bam_files=''
            vcf_command=''
    if bam_files!='' and not values.only_count and not values.only_sampleid:
        make_shell_file(values, bam_files, vcf_command,values.prefix+"_"+str(i))
    if values.only_count:
        print("\nBAMS:",bam_files, '\n\nVCFs:',vcf_command)
    print("\nTotal bams:", tot_bams, "\nTotal VCF:", tot_vcf)
    return bam_files, vcf_command


def go_through_directory(values):
    values.files=list()
    if values.filetype!='':
        words=values.filetype.split()
    else:
        words=['']
    if values.skip!=None:
        skip=values.skip.split()
    if values.sampleid_file!=None:
        filecands=list()
        with open(values.sampleid_file, encoding='utf-8') as f:
            for line in f.readlines():
                line=line.strip()
                if line.split(',')[1]==values.sample_type.strip():
                    filecands.append(line.split(',')[0][:12])
    for root, dirs, files in os.walk(values.directory, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
        for file in files: #Every file in the directory
            if not file.endswith('.bam'):
                continue
            in_file_cands=True
            if values.sampleid_file!=None:
                in_file_cands=False
                for cand in filecands:
                    if cand in file:
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
                    values.files.append(root+'/'+file)
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
    if values.directory!=None:
        if not os.path.isdir(values.directory): #Checks that destination directory exists
            optparser.error("Could not find directory "+values.directory+' from directory '+os.getcwd()+'.\n') #Directory was not found
        values = go_through_directory(values)
    assert values.prefix!=None, "Give prefix for files"
    return values


def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [command] [directory name]\n\
    Creates input file for muffinn.pl") #Make header for help page
    #Add options to parser
    optparser.add_option("-f", "--file", dest="files", help="File for mutation_load tool")
    optparser.add_option("--destination", dest="destination", default=os.getcwd(), help="destination to cdf file, report etc. (--destination /path/to/directory). Default is current directory")
    optparser.add_option("--vcf_location", dest="vcf_location", default="/csc/mustjoki/gatk/aa_genotype/annovar_g3_org/", help="Place to find vcf files")
    optparser.add_option("--bam_location", dest="directory", default="/csc/mustjoki/gatk/aa_genotype/gatk/", help="Directory containing bam files")
    optparser.add_option("--filetype", dest="filetype", default='', help="Files you want to be added in directory, for example JPN")
    optparser.add_option("--skip", dest="skip", help="Files you want to be skipped in directory, for example NIH")
    optparser.add_option("--only_count", dest="only_count", default=False, action="store_true", help="If you only want to count bam and vcf files")
    optparser.add_option("--only_sampleid", dest="only_sampleid", default=False, action="store_true", help="If you only want to print sample ids")
    optparser.add_option("--batch_size", dest="batch_size", type="int", default=100000, help="If you want to input permutations in batches for grun.py")
    optparser.add_option("--prefix", dest="prefix", help="Prefix for your shell files")
    optparser.add_option("--sampleid_file", dest="sampleid_file", help="If you have file containing wanted sample ids")
    optparser.add_option("--sample_type", dest="sample_type", help="AA, hMDS, healthy...")
    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    return check_optparsing(values, optparser)


def main():
    values=optparsing()
    bam_command, vcf_command= make_parameters(values)
    #shell_file=make_shell_file(values, bam_command, vcf_command,i)
    #os.system("qsub shell_file")

if __name__=='__main__':
    main()
