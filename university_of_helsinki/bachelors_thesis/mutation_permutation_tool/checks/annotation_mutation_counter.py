import optparse
import collections
import os
import re
import subprocess

#COUNTS HOW MANY MUTATIONS IN ANNOTATION FILE

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



def annotate_original(values, original_vcf, sample_id, prefix):
    print('time '+values.table_annovar+' '+original_vcf+' '
    +values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+
    values.destination+'/'+sample_id+'_'+prefix)
    size=0
    line_count=0
    vcf_line_count=get_line_count(original_vcf, True)
    i=0
    while not os.path.isfile(values.destination+'/'+sample_id+'_'+prefix+'.hg38_multianno.txt') or ((size==0 or line_count==1) and vcf_line_count!=1) or line_count!=vcf_line_count:
        os.system("rm "+values.destination+'/'+sample_id+'_'+prefix+'*')
        os.system('time '+values.table_annovar+' '+original_vcf+' '
        +values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+
        values.destination+'/'+sample_id+'_'+prefix)
        if os.path.isfile(values.destination+'/'+sample_id+'_'+prefix+'.hg38_multianno.txt'):
            line_count=get_line_count(values.destination+'/'+sample_id+'_'+prefix+'.hg38_multianno.txt', False)
            size=os.path.getsize(values.destination+'/'+sample_id+'_'+prefix+'.hg38_multianno.txt')
        if i>10:
            print("OBS! Error in "+prefix+" annotation, file "+original_vcf+". Original vcf line_count: "+str(vcf_line_count)+", size: "+str(size)+" New annotation line_count: "+str(line_count)+".")
            quit()
        i+=1
    return values.destination+'/'+sample_id+'_'+prefix+'.hg38_multianno.txt'



def find_original(values, sample_id):
    found=False
    found_file=""
    for root, dirs, files in os.walk("/csc/mustjoki/gatk/aa_genotype/annovar_g3_org_filter_vcf/"): #Goes through original directory and finds file that has same sample id in it
        for file in files:
            if not file.endswith(".vcf") or "NIH" in file or "JPN" in file or "CLV" in file:
                continue
            if sample_id in file:
                if "FHRB1641_BM_CD8" in sample_id:
                    if "sep13" in file:
                        if "sep13" in sample_id:
                            print(sample_id, file)
                            if found==False:
                                found=True
                                found_file=root+'/'+file
                            else:
                                print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
                    elif "jul12" in file:
                        if "jul12" in sample_id:
                            print(sample_id, file)
                            if found==False:
                                found=True
                                found_file=root+'/'+file
                            else:
                                print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
                    else:
                        if not "sep13" in sample_id and not "jul12" in sample_id:
                            print(sample_id, file)
                            if found==False:
                                found=True
                                found_file=root+'/'+file
                            else:
                                print("Refound: "+sample_id+" "+file+"  previous: "+found_file)

                elif "FHRB1641_BM_CD4" in sample_id:
                    if "sep13" in file:
                        if "sep13" in sample_id:
                            print(sample_id, file)
                            if found==False:
                                found=True
                                found_file=root+'/'+file
                            else:
                                print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
                    else:
                        if not "sep13" in sample_id:
                            print(sample_id, file)
                            if found==False:
                                found=True
                                found_file=root+'/'+file
                            else:
                                print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
                else:
                    if found==False:
                        found=True
                        found_file=root+'/'+file
                    else:
                        print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
    if not found:
        print("Did not found "+sample_id)
    return found_file



def check_mutations(values):
    sample_ids=list()
    perm_anno_files=dict()
    for root, dirs, files in os.walk(values.anno_perm_dir):
        for file in files: #Checks only VCF files that have permutations in root and saves them to dictionary with their sample id
            if not file.endswith(".hg38_multianno.txt") or not "_permutation_" in file:
                continue
            pattern=re.compile(r'.*_permutation_')
            matches=pattern.finditer(file)
            sample_id_found=False
            for match in matches:
                sample_id=match.group(0)[:-13]
                sample_ids.append(sample_id)
                sample_id_found=True
                perm_anno_files[sample_id]=root
                break
            if not sample_id_found:
                print("Could not find sample_id for permutated file "+file)
            break
    print("Total sample_ids: "+str(len(sample_ids)))
    return perm_anno_files, sample_ids


def count(anno_file):
    with open(anno_file, 'r') as f:
        lines=f.readlines()[1:]
    insertions=collections.Counter()
    deletions=collections.Counter()
    not_exonic=collections.Counter()
    synonymous=0
    nonsynonymous=0
    tot=0
    muut=0
    snv=0
    eri=0
    koko=0
    insertit2=collections.Counter()
    deli2=collections.Counter()
    for line in lines:
        if line.startswith('#'):
            continue
        koko+=1
        columns=line.split()
        if len(columns[3])>1 or columns[4]=='-':
            #if len(columns[3])==1:
            #    print(line)
            deletions[len(columns[3])]+=1
            deli2[len(columns[3]),columns[5]]+=1
            tot+=1
        elif len(columns[4])>1 or columns[3]=='-':
            insertions[len(columns[4])]+=1
            insertit2[len(columns[4]), columns[5]]+=1
            #if len(columns[4])==119:
                #print(line)
            tot+=1
        else:
            if columns[5]=="exonic":
                if columns[8]=="synonymous":
                    synonymous+=1
                    tot+=1
                    snv+=1
                elif columns[8]=="nonsynonymous":
                    nonsynonymous+=1
                    tot+=1
                    snv+=1
                else:
                    not_exonic[columns[8]]+=1
                    tot+=1
            else:
                not_exonic[columns[5]]+=1
                muut+=1
                tot+=1
    #print(tot, snv, deletions, insertions, synonymous, nonsynonymous, not_exonic, muut, eri, koko, insertit2, deli2)
    return tot, snv, deletions, insertions, synonymous, nonsynonymous, not_exonic, muut, eri, koko, insertit2, deli2


def compare_mutations(values):
    perm_anno_dirs, sample_ids=check_mutations(values)
    for sample_id in sample_ids:
        print("Comparing sample id "+sample_id)
        original_file=find_original(values, sample_id)
        annotated_orig=annotate_original(values, original_file, sample_id, "orig")
        orig_tot, orig_snv, orig_deletions, orig_insertions, orig_synonymous, orig_nonsynonymous, orig_not_exonic, orig_muut, orig_eri, orig_koko, orig_insertit2,\
         orig_deli2=count(annotated_orig)
        for root, dirs, files in os.walk(perm_anno_dirs[sample_id], topdown=True):
            for file in files:
                #annotated_perm=annotate_original(values, root+'/'+file, sample_id, "perm")
                annotated_perm=root+'/'+file
                tot, snv, deletions, insertions, synonymous, nonsynonymous, not_exonic, muut, eri, koko, insertit2, deli2=count(annotated_perm)
                if tot!=orig_tot:
                    print("Totals differ!!")
                    quit()
                if snv!=orig_snv:
                    print("SNV differ")
                    quit()
                for deletion in deletions:
                    if orig_deletions[deletion]!=deletions[deletion]:
                        print("Deletions differ!", deletion)
                        quit()
                for insertion in insertions:
                    if orig_insertions[insertion]!=insertions[insertion]:
                        print("Insertions differ!", insertion)
                        quit()
                if synonymous!=orig_synonymous:
                    print("Synonymous differ!")
                    quit()
                if nonsynonymous!=orig_nonsynonymous:
                    print("Nonsynonymous differ!")
                    quit()
                for thing in not_exonic:
                    if not_exonic[thing]!=orig_not_exonic[thing]:
                        print("Not exonic differ! ",thing)
                        quit()
                if muut!=orig_muut:
                    print("MUUT differ")
                    quit()
                if koko!=orig_koko:
                    print("KOKO differ!")
                    quit()
                #os.system("rm "+values.destination+'/'+sample_id+'_perm*')
                #break
        print("ALL matched with "+sample_id+", original file was "+original_file+" and permutated directory was",perm_anno_dirs[sample_id])
        os.system("rm "+values.destination+'/'+sample_id+'_orig*')

def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [command] [directory name]\n\
    Count mutations in annotated file") #Make header for help page
    optparser.add_option("-f", "--file", dest="file", help="File to analyze (-f /path/to/file)")
    optparser.add_option("--anno_perm_dir", dest="anno_perm_dir", default="/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/re_permutation/perm_annotations/", help="Path to anno_perm_dir")
    optparser.add_option("--destination", dest="destination",
    default="/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/re_permutation/temp/", help="Destination for annotation files")

    group = optparse.OptionGroup(optparser, "ANNOVAR options")
    group.add_option("--table_annovar", dest="table_annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/table_annovar.pl', help="Location of table_annovar.pl. Default: %default")
    group.add_option("--annovar", dest="annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/humandb_060418/', help="Location of annovar. Default: %default")
    group.add_option("--buildver", dest="buildver", default='hg38', help="Buildver version, default: %default")
    optparser.add_option_group(group)


    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    if values.file==None and values.anno_perm_dir==None: #Checks that either file or directory is given
        optparser.error("Give file (-f /path/to/file)") #Raises error if not
    return values

def main():
    values=optparsing()
    print("Starting analysis.")
    compare_mutations(values)
    print("Analysis ended.")

main()







#
# 8829 1284
# Counter({1: 1202, 2: 959, 4: 629, 3: 557, 5: 171, 6: 152, 8: 106, 10: 80, 12: 73, 7: 48, 14: 44, 9: 42, 16: 31, 15: 25, 11: 24, 13: 18, 22: 17, 17: 16, 20: 16, 18: 14, 19: 9, 24: 9, 23: 9, 21: 6, 25: 5, 28: 4, 26: 3, 29: 3, 34: 3, 32: 3, 60: 2, 27: 2, 30: 2, 33: 2, 31: 2, 39: 2, 49: 1, 40: 1, 35: 1, 43: 1, 37: 1, 69: 1, 55: 1, 202: 1})
# Counter({1: 1049, 2: 612, 4: 440, 3: 355, 5: 138, 6: 128, 8: 102, 12: 60, 7: 55, 10: 55, 9: 51, 11: 22, 15: 21, 16: 20, 14: 20, 13: 17, 19: 12, 18: 11, 20: 11, 21: 8, 22: 8, 27: 6, 23: 5, 24: 5, 25: 5, 26: 4, 17: 4, 30: 2, 40: 2, 31: 2, 36: 2, 74: 1, 33: 1, 28: 1, 29: 1, 45: 1, 39: 1, 42: 1, 59: 1, 41: 1, 57: 1, 51: 1, 61: 1, 46: 1, 32: 1, 120: 1})
# 745 539
# Counter({'intergenic': 24707, 'intronic': 18630, 'ncRNA_intronic': 2639, 'UTR3': 1447, 'downstream': 507, 'ncRNA_exonic': 506, 'upstream': 498, 'UTR5': 338, 'upstream;downstream': 37, 'splicing': 8, 'ncRNA_splicing': 1})
# 49318
