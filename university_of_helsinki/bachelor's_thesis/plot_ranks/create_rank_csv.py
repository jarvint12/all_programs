import csv

def create_muffinn_oncodrive(muffinn_lines, oncodrive_lines):
    muffinn_genes=list()
    for line in muffinn_lines:
        columns=line.split()
        muffinn_genes.append(columns[2])
    with open("/mnt/c/Users/TimoJ/Desktop/muffinn_oncodrivefm.csv", 'w+', newline='') as f_muff_dendr:
        writer=csv.writer(f_muff_dendr)
        rank=1
        for gene in muffinn_genes:
            rank2=1
            found=False
            for line in oncodrive_lines:
                columns=line.split()
                if columns[0]==gene:
                    writer.writerow([gene, str(rank), str(rank2)])
                    found=True
                    break
                rank2+=1
            if not found:
                writer.writerow([gene, str(rank), 10000])
            rank+=1

def create_dendrix_muffinn(dendrix_lines, muffinn_lines):
    dendrix_genes=list()
    for line in dendrix_lines:
        columns=line.split()
        for gene in columns[1:4]:
            if ',' in gene:
                continue
            if not gene in dendrix_genes:
                dendrix_genes.append(gene)
    with open("/mnt/c/Users/TimoJ/Desktop/dendrix_muffinn.csv", 'w+', newline='') as f_muff_dendr:
        writer=csv.writer(f_muff_dendr)
        rank=1
        for gene in dendrix_genes:
            rank2=1
            found=False
            for line in muffinn_lines:
                columns=line.split()
                if columns[2]==gene:
                    writer.writerow([gene, str(rank), str(rank2)])
                    found=True
                    break
                rank2+=1
            if not found:
                writer.writerow([gene, str(rank), 10000])
            rank+=1


def create_dendrix_oncodrive(dendrix_lines, oncodrive_lines):
    dendrix_genes=list()
    for line in dendrix_lines:
        columns=line.split()
        for gene in columns[1:4]:
            if ',' in gene:
                continue
            if not gene in dendrix_genes:
                dendrix_genes.append(gene)
                #if len(dendrix_genes)==50:
                #    break
        #if len(dendrix_genes)==50:
        #    break
    with open("/mnt/c/Users/TimoJ/Desktop/dendrix_oncodrive.csv", 'w+', newline='') as f_muff_dendr:
        writer=csv.writer(f_muff_dendr)
        rank=1
        for gene in dendrix_genes:
            rank2=1
            found=False
            for line in oncodrive_lines:
                columns=line.split()
                if columns[0]==gene:
                    writer.writerow([gene, str(rank), str(rank2)])
                    found=True
                    break
                rank2+=1
            if not found:
                writer.writerow([gene, str(rank), 10000])
            rank+=1


def main():
    f_muffinn=open("/mnt/c/Users/TimoJ/Desktop/DNsum_HRUH_AA.STRINGv10", 'r')
    muffinn_lines=f_muffinn.readlines()[1:]
    f_oncodrive= open("/mnt/c/Users/TimoJ/Desktop/aa_all_median-genes_sorted.txt", 'r')
    oncodrive_lines=f_oncodrive.readlines()[1:]
    f_dendrix=open("/mnt/c/Users/TimoJ/Desktop/sets_weightOrder_experiment_gene.txt")
    dendrix_lines=f_dendrix.readlines()
    create_muffinn_oncodrive(muffinn_lines, oncodrive_lines)
    create_dendrix_muffinn(dendrix_lines, muffinn_lines)
    create_dendrix_oncodrive(dendrix_lines, oncodrive_lines)
                #if rank>50:
                #    break
    f_muffinn.close()
    f_dendrix.close()
    f_oncodrive.close()

if __name__=='__main__':
    main()
