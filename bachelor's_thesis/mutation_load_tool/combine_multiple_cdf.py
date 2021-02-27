import optparse
import os
from datetime import datetime





def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [options]\n\
    Creates mutual CDF plot for multiple csv-files.") #Make header for help page
    optparser.add_option("-f", "--files", dest="files", help="CSV-files you want to combine")
    optparser.add_option("-d", "--destination", default=os.getcwd(), dest="destination", help="Destination for output file")
    optparser.add_option("--combine", dest="combine", default=False, action="store_true", help="If you want to combine multiple csv")
    optparser.add_option("--plot", dest="plot", default=False, action="store_true", help="If you want to plot file")
    optparser.add_option("--aa_file", dest="aa_file", help="If you want to get aa_files from csv-file.")
    (values, keys) = optparser.parse_args()
    return values, optparser


def main():
    values, optparser=optparsing()
    if values.combine:
        files=values.files.split()
        for file in files:
            if not os.path.isfile(file):
                optparser.error("Could not find file "+file+" from directory "+os.getcwd())
        with open(files[0], 'a') as f_w:
            for file in files[1:]:
                with open(file, 'r') as f_r:
                    lines=f_r.readlines()
                    for line in lines[1:]:
                        f_w.write(line)
    if values.plot:
        os.system('source /homes/tijarvin/anaconda3/bin/activate tijarvin_r ; Rscript mutation_load_multiple_cdf.R '+files[0]+datetime.now().strftime(" "+values.destination+"/cdf_fixed.jpg ")\
        + datetime.now().strftime(values.destination+"/cdf_fixed_%Y%m%dT%H%M%S.jpg")) #Gives 2 to program so it nows what to plot

    if values.aa_file!=None:
        sample_ids=list()
        csv_aa=list()
        with open(values.aa_file, 'r', encoding='utf-8') as fr: #Get sample_ids
            for line in fr.readlines()[1:]:
                columns=line.split(',')
                if columns[1].strip()=="AA":
                    sample_ids.append(columns[0])
        with open(values.files, 'r') as fr: #Write lines to new file that have sample id in them
            with open(values.destination+'/aa_cdf.csv', 'w+') as fw:
                lines=fr.readlines()
                fw.write(lines[0])
                for line in lines[1:]:
                    columns=line.split(',')
                    for sample_id in sample_ids:
                        if columns[0] in sample_id or "FHRB1641_BM_CD8" in columns[0] or "FHRB1641_BM_CD4" in columns[0]:
                            fw.write(line)
                            if not columns[0] in csv_aa: #Keep count how many samples have been written
                                csv_aa.append(columns[0])
                            break
        print(len(csv_aa), csv_aa)



if __name__=="__main__":
    main()
