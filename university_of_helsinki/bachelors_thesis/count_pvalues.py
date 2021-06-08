import os
import optparse


# python3 p_count.py -m /pathway_analysis/muffinn/MUFFINN-1.0.0/MUFFINN/output/permutation -d values.destination+/dendrix_output/ -o values.destination+'/onco_output' --treshold_m 0.945765809041326 --treshold_d 46 --treshold_o 1.5669621156177982*10**(-9)
# MUFFINN: 0.945765809041326, 0.690072737596779, 0.677729807856273, 0.661852072690863, 0.630459052612777, 0.229656174421512, 0.13222355743823
# Dendrix: 46, 45, 38, 22
# Onco: 1.5669621156177982e-09, 1.8536305823602106e-09, 2.594957804191722e-09, 3.810779358737193e-09, 5.9497309301548285e-09, 1.1701591044688264e-05, 4.175991203381191e-05
# print(1.5669621156177982*10**(-9)*1.8536305823602106*10**(-9))


def count_p_values(values, directory, treshold, column, headers, larger_better, ending, identifier):
    if values.skip!=None:
        files_to_skip=values.skip.split()
    p1=0
    p2=0
    total_files=0
    total_genes=0
    for root, dirs, files in os.walk(directory,  topdown=True):
        for file in files:
            if not identifier in file or not file.endswith(ending):
                continue
            if values.skip!=None:
                if file in files_to_skip:
                    continue
            first=True
            total_files+=1
            with open(root+'/'+file,'r') as f:
                i=0
                for line in f:
                    if i<headers:
                        i+=1
                        continue
                    total_genes+=1
                    columns=line.split()
                    try:
                        if (float(columns[column])>=treshold and larger_better) or (float(columns[column])<=treshold and not larger_better):
                            p2+=1
                            if first:
                                #print(root+'/'+file,columns[column],treshold)
                                p1+=1
                                first=False
                    except IndexError:
                        print(columns, column)

    return p1/total_files, p2/total_genes


def get_tresholds(result_file, top, column, headers):
    tresholds=list()
    with open(result_file, 'r') as fr:
        lines=fr.readlines()[headers:]
        i=0
        while i<top:
            columns=lines[i].split()
            tresholds.append(float(columns[column]))
            i+=1
    return tresholds



def check_optparsing(values, optparser):
    if values.muffinn==None and not values.skip_muffinn:
        optparser.error("Give directory containing MUFFINN outputs for permutated files (-m /path/to/directory)")
    elif values.muffinn!=None:
        if not os.path.isdir(values.muffinn): #Checks that destination directory exists
            optparser.error("Could not find directory "+values.muffinn+' from directory '+os.getcwd()+'.\n') #Directory was not found

    if values.dendrix==None and not values.skip_dendrix:
        optparser.error("Give directory containing Dendrix outputs for permutated files (-d /path/to/directory)")
    elif values.dendrix!=None:
        if not os.path.isdir(values.dendrix): #Checks that destination directory exists
            optparser.error("Could not find directory "+values.dendrix+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.oncodrive==None and not values.skip_onco:
        optparser.error("Give directory containing Oncodrive outputs for permutated files (-o /path/to/directory)")
    elif values.oncodrive!=None:
        if not os.path.isdir(values.oncodrive): #Checks that destination directory exists
            optparser.error("Could not find directory "+values.oncodrive+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.top==None:
        if values.treshold_m==None and not values.skip_muffinn:
            optparser.error("Give treshold for MUFFINN p-values (--treshold_m xx.xx)")
        if values.treshold_d==None and not values.skip_dendrix:
            optparser.error("Give treshold for Dendrix p-values (--treshold_d xx.xx)")
        if values.treshold_o==None and not values.skip_onco:
            optparser.error("Give treshold for Oncodrive-fm p-values (--treshold_d xx.xx)")

    if values.treshold_m!=None:
        values.treshold_m=[float(treshold) for treshold in values.treshold_m.split()]
    if values.treshold_d!=None:
        values.treshold_d=[float(treshold) for treshold in values.treshold_d.split()]
    if values.treshold_o!=None:
        values.treshold_o=[float(treshold) for treshold in values.treshold_o.split()]
    if values.top!=None:
        assert values.muffinn_results!=None or values.skip_muffinn, "Give MUFFINN result file to get tresholds"
        assert values.dendrix_results!=None or values.skip_dendrix, "Give Dendrix result file to get tresholds"
        assert values.onco_results!=None or values.skip_onco, "Give Oncodrive-fm result file to get tresholds"
        assert values.skip_muffinn or os.path.isfile(values.muffinn_results), "Could not find file "+values.muffinn_results+" from directory"+os.getcwd()+'.\n'
        assert values.skip_dendrix or os.path.isfile(values.dendrix_results), "Could not find file "+values.dendrix_results+" from directory"+os.getcwd()+'.\n'
        assert values.skip_onco or os.path.isfile(values.onco_results), "Could not find file "+values.onco_results+" from directory"+os.getcwd()+'.\n'
        if not values.skip_muffinn:
            if values.treshold_m!=None:
                values.treshold_m+=get_tresholds(values.muffinn_results, values.top, 9, 1)
            else:
                values.treshold_m=get_tresholds(values.muffinn_results, values.top, 9, 1)
        if not values.skip_dendrix:
            if values.treshold_d!=None:
                values.treshold_d+=get_tresholds(values.dendrix_results, values.top, 0, 0)
            else:
                values.treshold_d=get_tresholds(values.dendrix_results, values.top, 0, 0)
        if not values.skip_onco:
            if values.treshold_o!=None:
                values.treshold_o+=get_tresholds(values.onco_results, values.top, 1, 1)
            else:
                values.treshold_o=get_tresholds(values.onco_results, values.top, 1, 1)
    return values



def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [options]\n\
    Counts p-values for permutated outputs. Takes directories containing outputs and tresholds as values. Skips given files and all headers.") #Make header for help page

    group = optparse.OptionGroup(optparser, "Directories containing inputs for programs")
    group.add_option("-m", "--muffinn", dest="muffinn", help="Directory containing muffinn results for permutated files")
    group.add_option("-d", "--dendrix", dest="dendrix", help="Directory containing dendrix results for permutated files")
    group.add_option("-o", "--oncodrive", dest="oncodrive", help="Directory containing oncodrive results for permutated files")
    group.add_option("--skip", dest="skip", help="Files you want to skip")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "Tresholds")
    group.add_option("--treshold_m", dest="treshold_m", help="Treshold for muffinn outputs")
    group.add_option("--treshold_d", dest="treshold_d", help="Treshold for dendrix outputs")
    group.add_option("--treshold_o", dest="treshold_o", help="Treshold for oncodrive outputs")
    group.add_option("--skip_muffinn", dest="skip_muffinn", default=False, action="store_true", help="If you want to skip muffinn treshold")
    group.add_option("--skip_dendrix", dest="skip_dendrix", default=False, action="store_true", help="If you want to skip Dendrix treshold")
    group.add_option("--skip_onco", dest="skip_onco", default=False, action="store_true", help="If you want to skip Oncodrive-fm treshold")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "Program gets the tresholds from result files")
    group.add_option("--muffinn_results", dest="muffinn_results", help="File containing original MUFFINN results")
    group.add_option("--dendrix_results", dest="dendrix_results", help="File containing original Dendrix results")
    group.add_option("--onco_results", dest="onco_results", help="File containing original Oncodrive-fm results")
    group.add_option("--top", dest="top", type="int", help="How many top results you want")
    optparser.add_option_group(group)

    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    return check_optparsing(values, optparser)



def main():
    values=optparsing()
    if not values.skip_muffinn:
        for treshold_m in values.treshold_m:
            muffinn_p1, muffinn_p2=count_p_values(values, values.muffinn, treshold_m, 9,1, True, ".STRINGv10", "DNsum")
            print("With score "+str(treshold_m)+":\nP-value 1 for MUFFINN: ",str(muffinn_p1),".\n")
            print("P-value 2 for MUFFINN: ",str(muffinn_p2),".\n")
    if not values.skip_dendrix:
        for treshold_d in values.treshold_d:
            dendrix_p1, dendrix_p2=count_p_values(values, values.dendrix, treshold_d, 0, 0, True, ".txt", "sets_weightOrder_gene")
            print("With score "+str(treshold_d)+":\nP-value 1 for Dendrix: ",str(dendrix_p1),".\n")
            print("P-value 2 for Dendrix: ",str(dendrix_p2),".\n")
    if not values.skip_onco:
        for treshold_o in values.treshold_o:
            oncodrive_p1, oncodrive_p2=count_p_values(values, values.oncodrive, treshold_o, 1, 1, False, ".tsv", "median-genes")
            print("With score "+str(treshold_o)+":\nP-value 1 for Oncodrive-fm: ",str(oncodrive_p1),".\n")
            print("P-value 2 for Oncodrive-fm: ",str(oncodrive_p2),".\n")




if __name__=='__main__':
    main()
