import optparse
import os
import re

import patient_name


def find_sample_id(file):
    pattern=re.compile(r'(HRUH|FHRB)\d\d\d\d?_[A-Z]{2}\d?(_CD\d)?')
    matches=pattern.finditer(file)
    for match in matches:
        return match.group(0)
    else:
        return None


def move_files(values):
    aa_files=list()
    healthy_files=list()
    hMDS_files=list()
    not_found=list()
    found_columns=list()
    aa=hmds=healthy=others=0
    i=0
    with open(values.infofile, 'r') as f_r:
        lines=f_r.readlines()[1:]
    for root, dirs, files in os.walk(values.original_directory, topdown=True):
        for dir in dirs:
            if "aa_samples" in root or "aa_samples" in dir:
                continue
            sample_id=find_sample_id(dir)
            if sample_id==None:
                #print("SAMPLE_ID NOT FOUND", dir)
                continue
            for line in lines:
                columns=line.split(',')
                columns[1]=columns[1].strip()
                if sample_id in columns[0]:
                    if columns[1]=="AA":
                        i+=1
                        os.system("mv "+root+'/'+dir+" /csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/reports_permutation_HRUH/all_permutations/aa_samples/")
        continue
        if len(files)==0:
            continue
        #print(files)
        sample_id=find_sample_id(files[0])
        if sample_id==None:
            print("SAMPLE_ID NOT FOUND", files[0])
            continue
        sample_id_found=False
        for file in files:
            if not sample_id_found:
                for line in lines:
                    columns=line.split(',')
                    columns[1]=columns[1].strip()
                    if sample_id in columns[0]:
                        if columns[1]=="AA":
                            sample_type="AA"
                            aa_files.append(root+'/'+file)
                            aa+=1
                        elif columns[1]=='healthy':
                            sample_type="healthy"
                            healthy_files.append(root+'/'+file)
                            healthy+=1
                        elif columns[1]=='hMDS':
                            sample_type="hMDS"
                            hMDS_files.append(root+'/'+file)
                            hmds+=1
                        else:
                            sample_type=None
                            print("OUTOA!",columns[1])
                            break
                        sample_id_found=True
                        found_columns.append(columns[0])
            if not sample_id_found:
                #print(columns[0],files[0], sample_id)
                print(files[0])
                others+=1
                break
            #print(values.destination_directory+'/'+sample_type+'/'+file)
            #if not os.path.isdir(values.destination_directory+'/'+sample_type):
                #os.mkdir(values.destination_directory+'/'+sample_type)
            #if not os.path.isdir(values.destination_directory+'/'+sample_type+'/'+sample_id):
                #os.mkdir(values.destination_directory+'/'+sample_type+'/'+sample_id)
            #os.system("mv "+root+'/'+file+' '+values.destination_directory+'/'+sample_type+'/'+sample_id+'/'+file)
    print(i)
    return
    for line in lines:
        columns=line.split(',')
        if columns[0] not in found_columns:
            print(columns[0], columns[1].strip())
    print("AA:",aa_files)
    print("healthy:",healthy_files)
    print("hMDS:",hMDS_files)
    print(aa,healthy,hmds,others)



def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [options]\n\
    Moves permutated files to destination/AA, destination/hMDS and destination/healthy, depending of the sample type") #Make header for help page
    #Add options to parser
    optparser.add_option("-o", "--orig_dir", dest="original_directory", help="Directory containing all permutations")
    optparser.add_option("-i", "--infofile", dest="infofile", help="File containing info about sample ids and their types")
    optparser.add_option("-d", "--destination", dest="destination_directory", help="Directory where files are moved")
    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    if values.original_directory==None:
        optparser.error("Give directory containing the files (-o /path/to/directory)") #Raises error if not
    if values.infofile==None:
        optparser.error("Give file containing information of the files (-i /path/to/file)") #Raises error if not
    if values.destination_directory==None:
        optparser.error("Give directory where you want the files to be moved (-d /path/to/directory)") #Raises error if not
    return values


def main():
    values=optparsing()
    move_files(values)



if __name__=='__main__':
    main()
