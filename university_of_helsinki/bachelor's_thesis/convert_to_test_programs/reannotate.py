import os
import optparse
import re
import subprocess

def create_sub_shells(annotate_commands, j):

    if os.path.isfile("/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/annotations_shells_2/last_"+str(j)+'.sh'):
        print("Removed original shell file "+
        "/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/annotations_shells_2/last_"+str(j)+'.sh')
        os.system("rm "+"/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/annotations_shells_2/last_"+str(j)+'.sh')
    with open("/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/annotations_shells_2/last_"+str(j)+'.sh', 'w+') as fw:
        fw.write("#!/usr/bin/\n\n")
        fw.write("#$ -N reanno"+str(j)+"\n")
        fw.write("#$ -q all.q\n")
        fw.write("#$ -cwd\n")
        fw.write("#$ -e /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/qsub_output/annotations/re_"+str(j)+"_e.txt\n")
        fw.write("#$ -o /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/qsub_output/annotations/re_"+str(j)+"_o.txt\n")
        fw.write("source /homes/tijarvin/anaconda3/bin/activate tpyenv\n")
        fw.write(annotate_commands)
    #print("qsub "+values.destination+"/"+sample"+'.sh')
    os.system("qsub /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/annotations_shells_2/last_"+str(j)+'.sh')

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

def re_annotate(values):
    annotate_commands=""
    i=1000
    j=0
    for root, dirs, files in os.walk(values.directory, topdown=True):
        first=True
        for file in files:
            if not file.endswith(".hg38_multianno.txt"):
                continue
            if first:
                sample_id, sample_id_number, path_vcf=get_sample_number(file)
                line_amount_true=get_line_count(path_vcf, True)
                first=False
                for j in range(0,100):
                    if not os.path.isfile(root+'/'+sample_id+'_'+str(j)+'.hg38_multianno.txt'):
                        #print(root+'/'+sample_id+'_'+str(j)+'.hg38_dbnsfp33a_dropped')
                        #print(root+'/'+sample_id+'_'+str(j)+'.hg38_multianno.txt')
                        sample_id2, sample_id_number2, path_vcf2=get_sample_number(sample_id+'_'+str(j)+'.hg38_multianno.txt')
                        annotate_commands+="python3 annotate_given_file.py --sample_id "+sample_id2+" --sample_id_number "+sample_id2+'_'+str(j)+" --vcf_path "+path_vcf2+'; '
                        print(annotate_commands, i)
                        create_sub_shells(annotate_commands, i)
                        annotate_commands=""
                        i+=1
            line_amount=get_line_count(root+'/'+file, False)
            file_size=os.path.getsize(root+'/'+file)

            if line_amount!=line_amount_true and line_amount!=1 and file_size!=0:
                sample_id, sample_id_number, path_vcf=get_sample_number(file)
                line_amount_true2=get_line_count(path_vcf, True) #header
                if line_amount==line_amount_true2:
                    print("VCF-line counts differ, strange. First and "+path_vcf+'.')
                else:
                    print("Wrong line number "+root+'/'+file+": "+str(line_amount)+" vs "+path_vcf+": "+str(line_amount_true2))
                    line_amount=1

            if file_size==0 or line_amount==1:
                if file_size==0:
                    print("File size: "+str(file_size==0))
                else:
                    print("Line amount: "+str(line_amount))
                sample_id, sample_id_number, path_vcf=get_sample_number(file)
                annotate_commands+="rm "+root+'/'+file+"; python3 annotate_given_file.py --sample_id "+sample_id+" --sample_id_number "+sample_id_number+" --vcf_path "+path_vcf+'; '
                i+=1
                print(annotate_commands, i)
                create_sub_shells(annotate_commands, i)
                annotate_commands=""


                #if file.endswith(".invalid_input"):
                #    if file_size==0:
                #        os.system("rm "+root+'/'+file)

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
    optparser.add_option("--directory", dest="directory",
    default="/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool//reports_permutation_HRUH/all_permutations/aa_samples/annotations2/", help="Location of annotation files")
    optparser.add_option("--destination", dest="destination",
    default="/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool//reports_permutation_HRUH/all_permutations/aa_samples/annotations2/", help="Destination for annotation files")

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
    re_annotate(values)




if __name__=='__main__':
    main()
