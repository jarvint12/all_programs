import csv
import optparse
import os

def create_muffinn_oncodrive(values, muffinn_lines, oncodrive_lines):
    muffinn_genes=list()
    for line in muffinn_lines:
        columns=line.split()
        muffinn_genes.append(columns[2])
    with open(values.destination+"/muffinn_oncodrivefm.csv", 'w+', newline='') as f_muff_dendr:
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
                writer.writerow([gene, str(rank), str(len(oncodrive_lines)+10000)])
            rank+=1

def create_dendrix_muffinn(values, dendrix_lines, muffinn_lines):
    dendrix_genes=list()
    for line in dendrix_lines:
        columns=line.split()
        for gene in columns[1:4]:
            if ',' in gene:
                continue
            if not gene in dendrix_genes:
                dendrix_genes.append(gene)
    with open(values.destination+"/dendrix_muffinn.csv", 'w+', newline='') as f_muff_dendr:
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
                writer.writerow([gene, str(rank), str(len(muffinn_lines)+10000)])
            rank+=1


def create_dendrix_oncodrive(values, dendrix_lines, oncodrive_lines):
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
    with open(values.destination+"/dendrix_oncodrive.csv", 'w+', newline='') as f_muff_dendr:
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
                writer.writerow([gene, str(rank), str(len(oncodrive_lines)+10000)])
            rank+=1

def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [command] [directory name]\n\
    Sorts oncodrive output") #Make header for help page
    optparser.add_option("--muffinn_file", dest="muffinn_file", help="MUFFINN result file")
    optparser.add_option("--dendrix_file", dest="dendrix_file", help="Dendrix result file")
    optparser.add_option("--onco_file", dest="onco_file", help="Oncodrive-fm result file")
    optparser.add_option("--destination", dest="destination", default=os.getcwd(), help="Destination for rank files")
    (values, keys) = optparser.parse_args() #Separate values and keys from parser

    assert values.muffinn_file!=None and values.dendrix_file!=None and values.onco_file!=None, "Give all three files (muffinn, dendrix and oncodrive-fm result files)"
    assert os.path.isfile(values.muffinn_file), "Could not find file "+values.muffinn_file+" from directory "+os.getcwd()+"."
    assert os.path.isfile(values.dendrix_file), "Could not find file "+values.dendrix_file+" from directory "+os.getcwd()+"."
    assert os.path.isfile(values.onco_file), "Could not find file "+values.onco_file+" from directory "+os.getcwd()+"."
    assert os.path.isdir(values.destination), "Could not find directory "+values.destination+" from directory "+os.getcwd()+"."
    return values

def main():
    values=optparsing()
    f_muffinn=open(values.muffinn_file, 'r')
    muffinn_lines=f_muffinn.readlines()[1:]
    f_oncodrive= open(values.onco_file, 'r')
    oncodrive_lines=f_oncodrive.readlines()[1:]
    f_dendrix=open(values.dendrix_file, 'r')
    dendrix_lines=f_dendrix.readlines()
    create_muffinn_oncodrive(values, muffinn_lines, oncodrive_lines)
    create_dendrix_muffinn(values, dendrix_lines, muffinn_lines)
    create_dendrix_oncodrive(values, dendrix_lines, oncodrive_lines)
                #if rank>50:
                #    break
    f_muffinn.close()
    f_dendrix.close()
    f_oncodrive.close()

if __name__=='__main__':
    main()
