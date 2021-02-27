import os


#Rscript /mnt/c/Users/TimoJ/Documents/Atom_projects/hus_git/hus_hematology/Timo/bachelor_thesis/mutation_permutation_tool/mutation_load_coverages_multiple_files.R  /mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin\ yliopisto/daehong/cdf.20210219T174612.csv /mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin\ yliopisto/daehong/gene_cov.jpg /mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin\ yliopisto/daehong/gene_cov_zoomed.jpg
with open("/mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin yliopisto/daehong/HTLV2_list.csv", 'r') as fr:
    for line in fr:
        columns=line.split(',')
        os.system("sed -i \"s/^"+columns[1].strip()+"/"+columns[0].strip()+"/g\" /mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin\ yliopisto/daehong/cdf.20210219T174612.csv")
os.system("sed -i \"s/_PB//g\" /mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin\ yliopisto/daehong/cdf.20210219T174612.csv")
os.system("sed -i \"s/HTLV50351/HTLV2-2/g\" /mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin\ yliopisto/daehong/cdf.20210219T174612.csv")
os.system("sed -i \"s/HTLV50647/HTLV2-3/g\" /mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin\ yliopisto/daehong/cdf.20210219T174612.csv")
os.system("sed -i \"s/HTLV50311/HTLV2-1/g\" /mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin\ yliopisto/daehong/cdf.20210219T174612.csv")
