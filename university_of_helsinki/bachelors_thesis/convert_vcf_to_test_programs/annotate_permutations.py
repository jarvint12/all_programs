import os
import optparse

def create_annotation_shells(values, perm_directory_path, sample):
    if os.path.isfile(values.shell_dest+"/"+sample+".sh"):
        print("Removed original shell file "+values.shell_dest+"/"+sample+".sh.")
        os.system("rm "+values.shell_dest+"/"+sample+".sh")
    with open(values.shell_dest+"/"+sample+".sh", 'w+') as fw:
        fw.write("#!/usr/bin/\n\n")
        fw.write("#$ -N "+sample+"\n")
        fw.write("#$ -q all.q\n")
        fw.write("#$ -cwd\n")
        fw.write("#$ -e "+values.shell_dest+"/"+sample+"_e.txt\n")
        fw.write("#$ -o "+values.shell_dest+"/"+sample+"_o.txt\n")
        fw.write("source /homes/tijarvin/anaconda3/bin/activate tpyenv\n")
        fw.write("python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/annotate_permutation_dir.py --perm_directory "+ \
        perm_directory_path+" --destination "+values.anno_dest+" --sample "+sample+" --table_annovar "+values.table_annovar+" --annovar "+values.annovar+ \
        " --buildver "+values.buildver)
    #print("qsub "+values.shell_dest+"/"+sample"+'.sh')
    if values.submit_jobs:
        os.system("qsub "+values.shell_dest+"/"+sample+'.sh')

def go_through_directory(values):
    sum=0
    ready=list()
    for root, dirs, files in os.walk(values.anno_dest, topdown=True):
        for dir in dirs:
            ready.append(dir)
    print(ready)
    for root, dirs, files in os.walk(values.directory, topdown=True):
        for dir in dirs:
            sample=dir[:-13]
            if sample in ready or not "permutations" in dir or "new_AA_permutations_" in dir or "mutation_load_permutations" in dir:
                if sample in ready:
                    print("Annotations directory for sample "+sample+" was already found.")
                continue
            #print("'"+dir[:-13]+"'")
            found=False
            for root2, dirs2, files2 in os.walk(root+'/'+dir):
                for file2 in files2:
                    if "99" in file2:
                        found=True
                        sum+=1
            if found:
                if not values.only_print:
                    create_annotation_shells(values, root+'/'+dir, sample)
                else:
                    print(root+'/'+dir)
    print("Total:",sum)



def check_optparsing(optparser, values):
    if values.directory==None:
        optparser.error("Give file directory (--directory path/to/directory)") #Raises error if not
    if not os.path.isdir(values.directory): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.directory+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.shell_dest==None:
        optparser.error("Give destination directory (--shell_dest path/to/directory)") #Raises error if not
    if not os.path.isdir(values.shell_dest): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.shell_dest+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.anno_dest==None:
        optparser.error("Give destination directory for annotation files (--anno_dest path/to/directory)") #Raises error if not
    if not os.path.isdir(values.shell_dest): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.shell_dest+' from directory '+os.getcwd()+'.\n') #Directory was not found

def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [options]\n\
    Creates shell files for every permutation directory in the given directory. Then submits the shell files, which use annotate_permutation_dir.py \
    to annotate files in given directory") #Make header for help page

    optparser.add_option("--only_print", dest="only_print", default=False, action="store_true", help="If you only want to print wanted directories")
    optparser.add_option("--submit_jobs", dest="submit_jobs", default=False, action="store_true", help="If you want the program to submit shell scripts")

    group=optparse.OptionGroup(optparser, "Different input directories")
    group.add_option("--directory", dest="directory", help="Directory of the wanted permutation files")
    group.add_option("--shell_dest", dest="shell_dest", help="Destination for shell files")
    group.add_option("--anno_dest", dest="anno_dest", help="Destination for annotation files")
    optparser.add_option_group(group)

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
    go_through_directory(values)


if __name__=='__main__':
    main()
