import os
import optparse
import time


def run_programs(values):
    time_report=open(values.destination+'/time_report.txt', 'a+')
    dest_muffinn_output=values.destination+'/muffinn_output'
    if not os.path.isdir(dest_muffinn_output) and values.muffinn_run:
        try:
            os.mkdir(dest_muffinn_output)
        except FileExistsError:
            pass
    dest_onco_output=values.destination+'/onco_output'
    if not os.path.isdir(dest_onco_output) and values.onco_run:
        try:
            os.mkdir(dest_onco_output)
        except FileExistsError:
            pass
    dest_dendrix_output=values.destination+'/dendrix_output'
    if not os.path.isdir(dest_dendrix_output) and values.dendrix_run:
        try:
            os.mkdir(dest_dendrix_output)
        except FileExistsError:
            pass


    if values.muffinn_run:
        current_dir=os.getcwd()
        os.chdir(values.muffinn)
        i=values.run_start
        while i<=values.number:
            for root, dirs, files in os.walk(values.dest_muffinn, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
                for file in sorted(files):
                    if not "MUFFINN_input" in file:
                        continue
                    if "_"+str(i)+"_" in file:
                        starting_time=time.time()
                        print("perl muffinn.pl "+root+'/'+file+" permutation_output_"+str(i))
                        os.system("perl muffinn.pl "+root+'/'+file+" permutation_output_"+str(i))
                        time_report.write("Muffinn: "+str(time.time()-starting_time)+' seconds.\n')
                        os.system("mv "+values.muffinn+"/output/*permutation_output_"+str(i)+".* "+dest_muffinn_output+"/")
                        break
            i+=1
        os.chdir(current_dir)
    #os.system("rm "+values.muffinn+'/output/*HumanNet')
    if values.onco_run:
        i=values.run_start
        while i<=values.number:
            for root, dirs, files in os.walk(values.dest_onco, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
                for file in sorted(files):
                    if not file.endswith("_oncodrive.txt"):
                        continue
                    if "_"+str(i)+"_" in file:
                        starting_time=time.time()
                        print("source /homes/tijarvin/anaconda3/bin/activate permutation_mod; oncodrivefm -e median -o "+dest_onco_output+"/ -m /fs/vault/pipelines/gatk/bin/oncodrivefm_p3.6/data/hugo2go_kegg.txt \
                        -n permutation_"+str(i)+'_median '+root+'/'+file)
                        os.system("source /homes/tijarvin/anaconda3/bin/activate permutation_mod; oncodrivefm -e median -o "+dest_onco_output+"/ -m /fs/vault/pipelines/gatk/bin/oncodrivefm_p3.6/data/hugo2go_kegg.txt \
                        -n permutation_"+str(i)+'_median '+root+'/'+file)
                        time_report.write("Oncodrive: "+str(time.time()-starting_time)+' seconds.\n')
                        #os.system("python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/sort_onco.py -f permutation_"+str(i)+"_median-genes.tsv"+\
                        #" --destination "+dest_onco_output)
                        #os.system("python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/sort_onco.py -f permutation_"+str(i)+"_median-pathways.tsv"+\
                        #" --destination "+dest_onco_output)
                        break
            i+=1

    if values.dendrix_run:
        print("Running Dendrix")
        i=values.run_start
        versions=["gene"]#, "pathway"]
        while i<=values.number:
            print("i: "+str(i))
            input_file=None
            analyzed_file=None
            done=False
            for version in versions:
                for root, dirs, files in os.walk(values.dest_dendrix, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
                    for file in files:
                        if not file.endswith("."+version+".txt") and not file.endswith("_analyzed_"+version+"s.txt"):
                            continue
                        print("FILE:",file)
                        if ('_'+str(i)+'_') in file and version+".txt" in file:
                            print(version+".txt: "+root+'/'+file)
                            input_file=root+'/'+file
                        if ('_'+str(i)+'_') in file and "analyzed_"+version+"s.txt" in file:
                            print("analyzed.txt: "+root+'/'+file)
                            analyzed_file=root+'/'+file
                        if input_file!=None and analyzed_file!=None:
                            starting_time=time.time()
                            print("python2 "+values.dendrix+' '+input_file+" 3 1 1000000 "+analyzed_file+" 1 1000")
                            os.system("python2 "+values.dendrix+' '+input_file+" 3 1 1000000 "+analyzed_file+" 1 1000")
                            time_report.write("Dendrix: "+str(time.time()-starting_time)+' seconds.\n')
                            os.system("pwd")
                            os.system("ls")
                            print("mv sets_weightOrder_experiment0.txt "+dest_dendrix_output+'/permutation_'+str(i)+'_sets_weightOrder_'+version+'.txt')
                            print("mv sets_frequencyOrder_experiment0.txt "+dest_dendrix_output+'/permutation_'+str(i)+'_sets_frequencyOrder_'+version+'.txt')
                            os.system("mv sets_weightOrder_experiment0.txt "+dest_dendrix_output+'/permutation_'+str(i)+'_sets_weightOrder_'+version+'.txt')
                            os.system("mv sets_frequencyOrder_experiment0.txt "+dest_dendrix_output+'/permutation_'+str(i)+'_sets_frequencyOrder_'+version+'.txt')
                            done=True
                            break
                    if done:
                        break
            i+=1
    time_report.close()

# Adds every annotation file with given index to same input string, combines these with fusiation programs for MUFFINN, oncodrive-fm and Dendrix
def create_inputs(values):
    if not os.path.isdir(values.dest_muffinn):
        os.mkdir(values.dest_muffinn)
    if not os.path.isdir(values.dest_onco):
        os.mkdir(values.dest_onco)
    if not os.path.isdir(values.dest_dendrix):
        os.mkdir(values.dest_dendrix)
    if not os.path.isdir(values.destination+'/temp_anno'):
        os.mkdir(values.destination+'/temp_anno')
    i=values.start_num
    while i<=values.number:
        string="\""
        files=list()
        for root, dirs, files in os.walk(values.directory, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
            j=0
            for file in files: #Every file in the directory
                if "_"+str(i)+".hg38_multianno.txt" in file:
                    string+=root+'/'+file+' '
                    # while not os.path.isfile(values.destination+'/temp_anno/temp_'+str(j)+'_anno.hg38_multianno.txt'):
                    #     os.system(values.table_annovar+' '+root+'/'+file+' '+values.annovar+' -buildver '+values.buildver+\
                    #     ' -otherinfo -remove --vcfinput -protocol refGene -operation g -out '+values.destination+'/temp_anno/temp_'+str(j)+'_anno')
                    # file=values.destination+'/temp_anno/temp_'+str(j)+'_anno.hg38_multianno.txt'
                    # string+=values.destination+'/temp_anno/temp_'+str(j)+'_anno.hg38_multianno.txt '
                    j+=1
        string+="\""
        print("STRING: "+string)
        time.sleep(2)
        if not values.no_muffinn:
            starting_time=time.time()
            os.system("python3 "+values.vcf2muffinn+" -f "+string+" -x "+values.xref_file+" --destination "+values.dest_muffinn+ \
            ' --prefix permutated_'+str(i)+' --skip_anno')
            print("MUFFINN generation: "+str(time.time()-starting_time)+' seconds.\n')
        if not values.no_onco:
            while not os.path.isfile(values.dest_onco+'/permutated_'+str(i)+'_oncodrive.txt'):
                starting_time=time.time()
                os.system("python3 "+values.f_onco+" -f "+string+" --prefix permutated_"+str(i)+' --destination '+values.dest_onco) #'/csc/mustjoki2/variant_move/epi_ski/pathway_analysis/test_perm2mod/permutation2mod/onco_input/temp_fusiate.oncordive.txt'
            print("Onco generation: "+str(time.time()-starting_time)+' seconds.\n')
        if not values.no_dendrix:
            starting_time=time.time()
            os.system("python3 "+values.dendrix_multiple+" -f "+string+" --prefix permutated_"+str(i)+' --destination '+values.dest_dendrix)
            print("Dendrix generation: "+str(time.time()-starting_time)+' seconds.\n')
        print("DONE, "+str(j))
        #os.system("rm "+values.destination+'/permutation2mod/temp_anno/*')
        i+=1
    #os.system("rm -r"+values.destination+'/permutation2mod/temp_anno/')
    #os.system("rm "+values.destination+dest_dendrix+'/*gene.txt')


def check_optparsing(values, optparser):
    if values.destination==None: #Checks that either file or directory is given
        optparser.error("Give destination directory (--destination /path/to/directory)") #Raises error if not
    if not os.path.isdir(values.destination): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.destination+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if not os.path.isdir(values.destination+'/permutation2mod'):
        try:
            os.mkdir(values.destination+'/permutation2mod')
        except FileExistsError:
            pass
    values.destination+='/permutation2mod'

    if values.create_inputs:
        if values.directory==None: #Checks that either file or directory is given
            optparser.error("Give directory (-d /path/to/directory)") #Raises error if not
        if not os.path.isdir(values.directory): #Checks that destination directory exists
            optparser.error("Could not find directory "+values.directory+' from directory '+os.getcwd()+'.\n') #Directory was not found
        if values.xref_file==None: #Checks that either file or directory is given
            optparser.error("Give xref file (-x /path/to/file.xref)") #Raises error if not
        if not os.path.isfile(values.xref_file): #If file does not exist
            raise NameError("Could not find file "+values.xref_file+' from directory '+os.getcwd()+'.\n') #Raises error
        if values.vcf2muffinn==None: #Checks that either file or directory is given
            optparser.error("Give vcf2muffinn file (-x /path/to/file.py)") #Raises error if not
        if not os.path.isfile(values.vcf2muffinn): #If file does not exist
            raise NameError("Could not find file "+values.vcf2muffinn+' from directory '+os.getcwd()+'.\n') #Raises error
        if values.f_onco==None: #Checks that either file or directory is given
            optparser.error("Give fusiate_onco_input file (-x /path/to/file.py)") #Raises error if not
        if not os.path.isfile(values.f_onco): #If file does not exist
            raise NameError("Could not find file "+values.f_onco+' from directory '+os.getcwd()+'.\n') #Raises error
        if values.dendrix_multiple==None: #Checks that either file or directory is given
            optparser.error("Give dendrix_multiple_input file (-x /path/to/file.py)") #Raises error if not
        if not os.path.isfile(values.dendrix_multiple): #If file does not exist
            raise NameError("Could not find file "+values.dendrix_multiple+' from directory '+os.getcwd()+'.\n') #Raises error
        values.prog_input_dirs=values.destination
    elif values.run_programs:
        assert values.prog_input_dirs!=None, "Give directory containing input directories for MUFFINN, Oncodrive-fm and Dendrix"

    if not os.path.isdir(values.annovar): #Checks that annovar directory exists
        optparser.error("Could not find directory "+values.annovar+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if not os.path.isfile(values.table_annovar): #Checks that table_annovar.pl exists
        optparser.error("Could not find file "+values.table_annovar+' from directory '+os.getcwd()+'.\n') #Directory was not found

    if not os.path.isfile(values.dendrix): #If file does not exist
        raise NameError("Could not find file "+values.dendrix+' from directory '+os.getcwd()+'.\n') #Raises error
    if not os.path.isdir(values.muffinn): #If file does not exist
        raise NameError("Could not find directory "+values.muffinn+' from directory '+os.getcwd()+'.\n') #Raises error

    if values.create_inputs or values.run_programs:
        values.dest_muffinn=values.prog_input_dirs+'/muffinn_input'
        values.dest_onco=values.prog_input_dirs+'/onco_input'
        values.dest_dendrix=values.prog_input_dirs+'/dendrix_input'
    return values



def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog --directory example/dir/ --destination example/dir/2/ --number 99  [options]\n\
    Creates input file for MUFFINN, Dendrix and Oncodrive-fm from mutation_load.py outputs") #Make header for help page
    optparser.add_option("--number", dest="number", type="int", default=99, help="What is the biggest index for permutated vcf files. Default: %default")
    optparser.add_option("--start_num", dest="start_num", type="int", default=0, help="The first index you want to start with permutated vcf files. Default: %default")
    optparser.add_option("--run_programs", dest="run_programs", action="store_true", default=False, help="If you want to the program to run created inputs. Default: %default")
    optparser.add_option("--create_inputs", dest="create_inputs", action="store_true", default=False, help="If you want to the program to create inputs. Default: %default")
    optparser.add_option("--run_start", dest="run_start", type="int", default=0, help="The first index of input file for test programs. Default: %default")

    group = optparse.OptionGroup(optparser, "Directory options",
                    "Directories like location of permutated files, destination directory etc.")
    optparser.add_option("-d", "--directory", dest="directory", help="Directory containing files permutated files")
    optparser.add_option("--destination", dest="destination", help="destination for output files")
    optparser.add_option("--prog_input_dirs", dest="prog_input_dirs", help="destination for test program input file directories. Give if you don't give --create_inputs")

    group = optparse.OptionGroup(optparser, "Mutation enrichment programs' settings",
                    "Paths for example to fusiation scripts and test program folders")
    group.add_option("-x", "--xref", dest="xref_file", help="MUFFINN xref file for genes (-x /path/to/file)")
    group.add_option("--vcf2muffinn", dest="vcf2muffinn", help="path to vcf2muffinn.py (-vcf2muffinn /path/to/file.py)")
    group.add_option("--f_onco", dest="f_onco", help="path to fusiate_onco_input.py (-f_onco /path/to/file.py)")
    group.add_option("--dendrix_multiple", dest="dendrix_multiple", help="path to dendrix_multiple_input.py (-dendrix /path/to/file.py)")
    group.add_option("--muffinn", dest="muffinn", default="/csc/mustjoki2/variant_move/epi_ski/pathway_analysis/muffinn/MUFFINN-1.0.0/MUFFINN", help="path to MUFFINN directory (-muffinn /path/to/MUFFINN)")
    group.add_option("--dendrix", dest="dendrix", default="/csc/mustjoki2/variant_move/epi_ski/pathway_analysis/dendrix/Dendrix/Dendrix.py", help="path to dendrix (-dendrix /path/to/dendrix.py)")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "Which program inputs to generate and run, default is all")
    group.add_option("--no_muffinn", dest="no_muffinn", action="store_true", default=False, help="If you don't want to generate MUFFINN input")
    group.add_option("--no_dendrix", dest="no_dendrix", action="store_true", default=False, help="If you don't want to generate Dendrix input")
    group.add_option("--no_onco", dest="no_onco", action="store_true", default=False, help="If you don't want to generate Oncodrive-fm input")
    group.add_option("--onco_run", dest="onco_run", action="store_true", default=False, help="If you want to run oncodrive-fm")
    group.add_option("--muffinn_run", dest="muffinn_run", action="store_true", default=False, help="If you want to run MUFFINN")
    group.add_option("--dendrix_run", dest="dendrix_run", action="store_true", default=False, help="If you want to run Dendrix")

    group = optparse.OptionGroup(optparser, "ANNOVAR options, probably not needed after all")
    group.add_option("--table_annovar", dest="table_annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/table_annovar.pl', help="Location of table_annovar.pl. Default: %default")
    group.add_option("--reference", dest="reference", default='/fs/vault/pipelines/gatk/data/homo_sapiens_v94/Homo_sapiens.GRCh38.dna.primary_assembly.fa', help="Reference fasta file (--reference /path/to/reference). Default: %default")
    group.add_option("--annovar", dest="annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/humandb_060418/', help="Location of annovar. Default: %default")
    group.add_option("--buildver", dest="buildver", default='hg38', help="Buildver version, default: %default")
    optparser.add_option_group(group)

    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    return check_optparsing(values, optparser)



def main():
    values=optparsing()
    if values.create_inputs:
        create_inputs(values)
    if values.run_programs:
        run_programs(values)


if __name__=='__main__':
    main()
