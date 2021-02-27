import os
import optparse

def create_annotation_shells(values,root, dir):
    sample=dir[:-13]
    path=root+'/'+dir
    if os.path.isfile(values.destination+"/"+sample+".sh"):
        print("Removed original shell file "+values.destination+"/"+sample+".sh.")
        os.system("rm "+values.destination+"/"+sample+".sh")
    with open(values.destination+"/"+sample+".sh", 'w+') as fw:
        fw.write("#!/usr/bin/\n\n")
        fw.write("#$ -N "+sample+"\n")
        fw.write("#$ -q all.q\n")
        fw.write("#$ -cwd\n")
        fw.write("#$ -e /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/qsub_output/annotations/"+sample+"_e.txt\n")
        fw.write("#$ -o /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/qsub_output/annotations/"+sample+"_o.txt\n")
        fw.write("source /homes/tijarvin/anaconda3/bin/activate tpyenv\n")
        fw.write("python3 annotate_permutation_dir.py --directory "+path+" --destination "+values.anno_dest+" --sample "+sample+\
        " --table_annovar "+values.table_annovar+" --annovar "+values.annovar+" --buildver "+values.buildver)
    #print("qsub "+values.destination+"/"+sample"+'.sh')
    os.system("qsub "+values.destination+"/"+sample+'.sh')

def go_through_directory(values):
    ready=list()
    for root, dirs, files in os.walk("/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/annotations2/", topdown=True):
        for dir in dirs:
            ready.append(dir)
    print(ready)
    for root, dirs, files in os.walk(values.directory, topdown=True):
        for dir in dirs:
            if dir[:-13] in ready or not "permutations" in dir:
                if dir[:-13] in ready:
                    print("Annotations directory for sample "+dir[:-13]+" was already found.")
                continue
            #print("'"+dir[:-13]+"'")
            create_annotation_shells(values, root, dir)



def check_optparsing(optparser, values):
    if values.directory==None:
        optparser.error("Give file directory (--directory path/to/directory)") #Raises error if not
    if not os.path.isdir(values.directory): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.directory+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.destination==None:
        optparser.error("Give destination directory (--destination path/to/directory)") #Raises error if not
    if not os.path.isdir(values.destination): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.destination+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.anno_dest==None:
        optparser.error("Give destination directory for annotation files (--anno_dest path/to/directory)") #Raises error if not
    if not os.path.isdir(values.destination): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.destination+' from directory '+os.getcwd()+'.\n') #Directory was not found

def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [options]\n\
    Creates shell files for every permutation directory in the given directory. Then submits the shell files, which use annotate_permutation_dir.py \
    to annotate files in given directory") #Make header for help page
    optparser.add_option("--directory", dest="directory", help="Directory of the wanted permutation files")
    optparser.add_option("--shell_dest", dest="destination", help="Destination for shell files")
    optparser.add_option("--anno_dest", dest="anno_dest", help="Destination for annotation files")

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
