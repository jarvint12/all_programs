import os
import time
import subprocess


for i in range(0,100):
    if os.path.isfile("mod_run"+str(i)+".ER"):
        os.system("rm mod_run"+str(i)+".*")
    os.system("grun.py -n mod_run"+str(i)+" -q all.q -c \"rm -r /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final2/temp/"+str(i)+
    "; mkdir /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final2/temp/"+str(i)+"; cd /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final2/temp/"+
    str(i)+"; source /homes/tijarvin/anaconda3/bin/activate tpyenv; python3 /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/permutation2mod.py "+
    "--number "+str(i)+" --run_start "+str(i)+" --destination /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final2/  "+
    "--run_programs --dendrix_run --prog_input_dirs /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/permutation2mod/\"") #mkdir /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final2/temp/"+str(i)+"
#     line_amount1=-1
#     line_amount2=-1
#     file="/csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/permutation2mod/dendrix_input/permutated_"+str(i)+"_dendrix_multiple_input.gene.txt"
#     file2="/csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/permutation2mod/dendrix_input/permutated_"+str(i)+"_dendrix_multiple_input.pathway.txt"
#     if os.path.isfile(file):
#         out=subprocess.Popen(["cat "+file+" | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
#         stdout, stderr=out.communicate()
#         line_amount1=int(stdout.split()[0].decode('utf-8'))
#     if os.path.isfile(file2):
#         out=subprocess.Popen(["cat "+file2+" | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
#         stdout, stderr=out.communicate()
#         line_amount2=int(stdout.split()[0].decode('utf-8'))
#     if line_amount1<51 or line_amount2<51:
#         print(file, line_amount1, line_amount2)
#         os.system("rm /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/permutation2mod/dendrix_input/permutated_"+str(i)+"_*")
#         os.system("rm /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/log/mod_gen"+str(i)+".* ")
#         os.system("grun.py -n mod_gen"+str(i)+" -q all.q -c \"source /homes/tijarvin/anaconda3/bin/activate tpyenv; python3 "+
#         "/csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/permutation2mod.py "+
#         "--f_onco /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/fusiate_onco_input.py "+
#         "--dendrix_multiple /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/dendrix_multiple_input.py"+
#         " --vcf2muffinn /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/vcf2muffinn.py "+
#         "-x /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/muffinn/hs_18499.CCDS.xref  --number "+str(i)+" --start_num "+str(i)+" --destination /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/  "+
#         "-d /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/annotations2/ --no_muffinn --no_onco --create_inputs\"")



    # file="/csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/permutation2mod/onco_input/permutated_"+str(i)+"_oncodrive.txt"
    # line_amount=-1
    # if os.path.isfile(file):
    #     out=subprocess.Popen(["cat "+file+" | wc -l"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
    #     stdout, stderr=out.communicate()
    #     line_amount=int(stdout.split()[0].decode('utf-8'))
    #
    # if line_amount<94943319:
    #     print(file, line_amount)
    #     os.system("rm /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/permutation2mod/onco_input/permutated_"+str(i)+"_*")
    #     os.system("rm /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/log/omod_gen"+str(i)+".* ")
    #     os.system("grun.py -n omod_gen"+str(i)+" -q all.q -c \"source /homes/tijarvin/anaconda3/bin/activate tpyenv; python3 "+
    #     "/csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/permutation2mod.py "+
    #     "--f_onco /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/fusiate_onco_input.py "+
    #     "--dendrix_multiple /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/dendrix_multiple_input.py"+
    #     " --vcf2muffinn /csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/convert_vcf_to_test_programs/vcf2muffinn.py "+
    #     "-x /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/muffinn/hs_18499.CCDS.xref  --number "+str(i)+" --start_num "+str(i)+" --destination /csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/  "+
    #     "-d /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/annotations2/ --no_muffinn --no_dendrix --create_inputs\"")

    #if not os.path.isfile("/csc/mustjoki2/variant_move/epi_ski/pathway_analysis/final/permutation2mod/onco_input/permutated_"+str(i)+"_dendrix_multiple_input.pathway.txt"):


    time.sleep(1)
