import os
import optparse
import time


#RNA data: /csc/mustjoki/gatk/rcc_tumor/, TURHA TIEDOSTO?`??`
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


def filter_vcf(values):
    for root, dirs, files in os.walk(values.directory, topdown=True):
        for file in files:
            vcf_line_count=get_anno_line_count(file, True)
            line_count=0
            while not os.path.isfile(values.destination+'/'+file+'.hg38_multianno.txt') or line_count!=vcf_line_count:
                print('time '+values.table_annovar+' '+root+'/'+file+' '
                +values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+
                values.destination+'/'+file)
                os.system('time '+values.table_annovar+' '+root+'/'+file+' '
                +values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+
                values.destination+'/'+file)
                if os.path.isfile(values.destination+'/'+file+'.hg38_multianno.txt'):
                    line_count=get_anno_line_count(values.destination+'/'+file+'.hg38_multianno.txt', False)
            os.system("grep '#' "+root+'/'+file+" > "+values.destination+'/'+file[:-4]+'_aa_mutations.vcf')
            with open(values.destination+'/'+file+'.hg38_multianno.txt', 'r') as f_anno:
                with open(values.destination+'/'+file[:-4]+'_aa_mutations.vcf', 'a') as fw:
                    for line in f_anno.readlines()[1:]:
                        columns=line.replace('\"', '').split()
                        if columns[5]=="exonic" and columns[8]!="synonymous" and columns[8]!="nonframeshift":
                            fw.write(line)
    os.system("rm "+values.destination+'/*.hg38_multianno*')
    os.system("perl /fs/vault/pipelines/gatk/src/1.0/run_variant_filter.pm - VCF "+values.destination+" annovar_g3")


def check_optparsing(optparser, values):
    if values.directory==None:
        optparser.error("Give file directory (-d path/to/directory)") #Raises error if not
    if not os.path.isdir(values.directory): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.directory+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.destination==None:
        optparser.error("Give destination directory (-d path/to/directory)") #Raises error if not
    if not os.path.isdir(values.destination): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.destination+' from directory '+os.getcwd()+'.\n') #Directory was not found

def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [options]\n\
    Gets directory as parameter and annotates every file in it") #Make header for help page
    optparser.add_option("--directory", dest="directory", help="Location of annotation files")
    optparser.add_option("--destination", dest="destination", help="Destination for annotation files")

    group = optparse.OptionGroup(optparser, "ANNOVAR options")
    group.add_option("--table_annovar", dest="table_annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/table_annovar.pl', help="Location of table_annovar.pl. Default: %default")
    group.add_option("--annovar", dest="annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/humandb_060418/', help="Location of annovar. Default: %default")
    group.add_option("--buildver", dest="buildver", default='hg38', help="Buildver version, default: %default")
    optparser.add_option_group(group)

    (values, keys) = optparser.parse_args()
    check_optparsing(optparser, values)
    return values

def main():
    values=optparsing()
    filter_vcf(values)


if __name__=='__main__':
    main()
