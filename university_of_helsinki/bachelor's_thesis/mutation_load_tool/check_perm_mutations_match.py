import os
import subprocess
import re


#Finds sample_id
def sample_id_vcf_aa(file):
    sample_id="Unknown"
    pattern_patient=re.compile(r'(HRUH|FH).*_(\w\w_\w\w\d_|\d\d?_(\w|\d)\d_|CD(4|8)_)(\w\w\w\d\d_|\d\d-\d\d_)?([a-z]{3}\d{2}_)?') #Tries to find Epi-Ski-type sample_id HRUH581_PB_CD4 FH_6288_2_D1 FHRB_892_2_D1 FHRB3801_BM_CD4_jul14 FHRB3696_MNC_3_14 FHRB613_PB_CD8 FHRB1182_CD4. Last group is for month.
    matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    for match in matches_sampleid:
        sample_id=match.group(0)[:-1]
    return sample_id


#Counts how many mutations there are on both files
def compare_mutations(orig_perm_dir, orig_vcf):
    p = subprocess.Popen('cat '+orig_vcf+' | grep -v \'#\' | wc -l', shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    out, err = p.communicate()
    orig_mutations=int(out.decode().strip())
    for root, dirs, files in os.walk(orig_perm_dir, topdown=True):
        for file in files:
            p = subprocess.Popen('cat '+root+'/'+file+' | grep -v \'#\' | wc -l', shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
            out, err = p.communicate()
            if orig_mutations!=int(out.decode().strip()):
                print("Mutations differ with "+root+'/'+file+", "+out.decode().strip()+" and "+orig_vcf+", "+str(orig_mutations))
                break


def check_mutations():
    sample_ids=list()
    permutated_files=dict()
    for root, dirs, files in os.walk("/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/"):
        for file in files: #Checks only VCF files that have permutations in root and saves them to dictionary with their sample id
            if not "_permutations" in root or not file.endswith(".vcf"):
                continue
            pattern=re.compile(r'.*_permutated_')
            matches=pattern.finditer(file)
            for match in matches:
                sample_id=match.group(0)[:-12]
                sample_ids.append(sample_id)
                permutated_files[sample_id]=root
            break
    for sample_id in sample_ids: #Goes through the list of files
        found=False
        found_file=""
        for root, dirs, files in os.walk("/csc/mustjoki/gatk/aa_genotype/annovar_g3_org/"): #Goes through original directory and finds file that has same sample id in it
            for file in files:
                if not file.endswith(".vcf") or "NIH" in file or "JPN" in file or "CLV" in file:
                    continue
                if sample_id in file:
                    if "FHRB1641_BM_CD8" in sample_id:
                        if "sep13" in file:
                            if "sep13" in sample_id:
                                print(sample_id, file)
                                if found==False:
                                    compare_mutations(permutated_files[sample_id], root+'/'+file)
                                    found=True
                                    found_file=file
                                else:
                                    print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
                        elif "jul12" in file:
                            if "jul12" in sample_id:
                                print(sample_id, file)
                                if found==False:
                                    compare_mutations(permutated_files[sample_id], root+'/'+file)
                                    found=True
                                    found_file=file
                                else:
                                    print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
                        else:
                            if not "sep13" in sample_id and not "jul12" in sample_id:
                                print(sample_id, file)
                                if found==False:
                                    compare_mutations(permutated_files[sample_id], root+'/'+file)
                                    found=True
                                    found_file=file
                                else:
                                    print("Refound: "+sample_id+" "+file+"  previous: "+found_file)

                    elif "FHRB1641_BM_CD4" in sample_id:
                        if "sep13" in file:
                            if "sep13" in sample_id:
                                print(sample_id, file)
                                if found==False:
                                    compare_mutations(permutated_files[sample_id], root+'/'+file)
                                    found=True
                                    found_file=file
                                else:
                                    print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
                        else:
                            if not "sep13" in sample_id:
                                print(sample_id, file)
                                if found==False:
                                    compare_mutations(permutated_files[sample_id], root+'/'+file)
                                    found=True
                                    found_file=file
                                else:
                                    print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
                    else:
                        if found==False:
                            compare_mutations(permutated_files[sample_id], root+'/'+file)
                            found=True
                            found_file=file
                        else:
                            print("Refound: "+sample_id+" "+file+"  previous: "+found_file)
        if not found:
            print("Did not found "+sample_id)

            # if sample_id==None:
            #     print("Sample id not found from permutated file "+file)
            # if sample_id not in original_files:
            #     print("Sample_id: "+sample_id+" from file "+file+" was not found in original files.")
            # break
            #


#Collects all HRUH/FH samples from the directory, prints if sample_id was not found or if 2 files have same sample id
def get_original_vcf():
    original_files=dict()
    for root, dirs, files in os.walk("/csc/mustjoki/gatk/aa_genotype/annovar_g3_org/"):
        for file in files:
            if not file.endswith(".vcf") or "NIH" in file or "JPN" in file or "CLV" in file:
                continue
            sample_id=sample_id_vcf_aa(file)
            if sample_id==None:
                print("Sample id not found "+file)
            else:
                if sample_id in original_files:
                    print("Same sample_id: "+sample_id+", "+file+", "+original_files[sample_id])
                else:
                    original_files[sample_id]=root+'/'+file
    return original_files



def main():
    #original_files=get_original_vcf()
    #print(original_files)
    check_mutations()


if __name__=='__main__':
    main()
