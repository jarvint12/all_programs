import os
import optparse
import time


def get_line_count(file, is_vcf):
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

def get_sample_number(file):
    sample_id_number=file[:-19]
    pattern=re.compile('_\d\d?$')
    matches=pattern.finditer(sample_id_number)
    for match in matches:
        number=match.group(0)
    sample_id=sample_id_number[:-len(number)]
    vcf_file=sample_id+"_permutated"+number+'.vcf'
    path_vcf="/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/"+sample_id+"_permutations/"+vcf_file
    return sample_id, sample_id_number, path_vcf


def annotate_directory(values):
    i=0
    if not os.path.isdir(values.destination+'/'+values.sample):
        os.mkdir(values.destination+'/'+values.sample)
    for root, dirs, files in os.walk(values.directory, topdown=True):
        for file in files:
            sample_id, sample_id_number, path_vcf=get_sample_number(file)
            size=0
            line_count=0
            vcf_line_count=get_line_count(path_vcf, True)
            while not os.path.isfile(values.destination+'/'+sample_id+'/'+sample_id_number+'.hg38_multianno.txt') or size==0 or line_count==1 or line_count!=vcf_line_count:
                os.system("rm "+values.destination+'/'+sample_id+'/'+sample_id_number+'*')
                print('time '+values.table_annovar+' '+root+'/'+file+' \
                '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f \
                -out '+values.destination+'/'+values.sample+'/'+values.sample+'_'+str(i))
                os.system('time '+values.table_annovar+' '+root+'/'+file+' \
                '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f \
                -out '+values.destination+'/'+values.sample+'/'+values.sample+'_'+str(i))
                time.sleep(1)
                if os.path.isfile(values.destination+'/'+sample_id+'/'+sample_id_number+'.hg38_multianno.txt'):
                    line_count=get_line_count(values.destination+'/'+sample_id+'/'+sample_id_number+'.hg38_multianno.txt', False)
                    size=os.path.getsize(values.destination+'/'+sample_id+'/'+sample_id_number+'.hg38_multianno.txt')

            os.system("rm "+values.destination+'/'+values.sample+'/'+values.sample+'_'+str(i)+".avinput "\
            +values.destination+'/'+values.sample+'/'+values.sample+'_'+str(i)+".hg38_multianno.vcf")
            i+=1

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
    optparser.add_option("--directory", dest="directory", help="Directory of the wanted permutation files")
    optparser.add_option("--destination", dest="destination", help="Destination for shell files")
    optparser.add_option("--sample", dest="sample", help="Sample id of the directory")

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
    annotate_directory(values)


if __name__=='__main__':
    main()
