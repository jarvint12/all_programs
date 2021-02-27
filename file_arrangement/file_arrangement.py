import re
import os
import shutil
import optparse
from colorama import Back
import shlex
import time
import datetime
import hashlib
import configparser
import os

parser=configparser.ConfigParser()
parser.read('file_arrangement_config.ini') #Read config-file
vcf_destination = parser.get('other','vcf_destination') #Directory where vcf-files are moved
annotation=parser.get('folders','folder_annotation') #Directory where annotation-files are moved
log_folder=parser.get('other','log_folder') #Directory where the log-files are moved
unidentified_file=parser.get('other','file_for_unidentified') #File where unidentified files are moved


#Makes report and unidentified files if it doesn't exist yet
def make_files(values, currentDT, ignored_directories, ignored_files):
    report = "file_arrangement_report"+currentDT.strftime("%Y%m%dT%H%M%S")+".txt" #Report name with timestamp
    ignored_files.append(report) #Program ignores report
    report_name=values.dst+'/'+report #Report with path
    with open(report_name, 'w+') as f: #Makes report and writes header
        f.write("File_arrangement.py report, "+currentDT.strftime("%Y-%m-%d %H:%M:%S")+". Moved files from directory "+values.src+" to directory (dest) "+values.dst+".\n"+\
        "Ignored directories, if any: "+str(ignored_directories)+". Ignored files, if any: "+str(ignored_files)+".\n"+\
        "Files are listed like this: root/file ---> dest/path/to/file. Old file location can be found above of the file on line 'In directory (root): /some/path'\n\n")

    unidentified_files = os.getcwd()+'/'+unidentified_file #unidentified_file is made to source-directory. All unidentified files are written there.
    if not os.path.isfile(unidentified_files):#Checks if file exists already
        with open(unidentified_files, 'w+') as f: #Create file where unidentified files will be written
            f.write("##Here are all unidentified files. Replace XXX with sample_id, if you want it to be moved next time the program runs. If you want to skip the file for now, leave XXX untouched.\n"+\
            "##If the first parameter is \"unknown\", program doesn't know where the file should be moved in sample_id-directory.\n"+\
            "##Replace \"unknown\" with the destination directory (")
            path_items = parser.items("folders")
            for key, folder in path_items: #List every possible folder where files can be moved in sample_id directory
                f.write(folder+', ')
            f.seek(f.tell()-2, os.SEEK_SET) #Deletes last comma
            f.write(" or "+vcf_destination+") or leave it untouched if you want to skip that file for know.\n"+ #vcf-destination is not in the defaults, at least yet
            "##And be careful not to touch commas and original file path. Only thing you should change is XXX and/or destination ('unknown').\n\n")

    return report_name, unidentified_files, ignored_files #Returns names of the files to main-function


#If file is unidentifies, it is written to unidentified files in format directory,root/to/file,sample_id, where directory may be unknown and sample_id XXX
def write_unidentified_file(directory, root, file, sample_id, report_name):
    with open(os.getcwd()+'/'+unidentified_file, 'a+') as f: #Write file to text file
        f.seek(0) #File can be read
        if not root+'/'+file in f.read(): #Doesn't write duplicates. Writes unidentified file to text file with known parameters
            if directory==None and sample_id==None: #Directory and sample_id couldn't be identified
                f.write("unknown,"+root+'/'+file+",XXX"+'\n')
            elif directory==None: #Only directory couldn't be identified
                f.write("unknown,"+root+'/'+file+','+sample_id+'\n')
            elif sample_id==None: #Only sample_id couldn't be identified
                f.write(directory+","+root+'/'+file+",XXX"+'\n')
            else: #Both could be identified
                f.write(directory+","+root+'/'+file+','+sample_id+'\n')
            with open(report_name, 'a') as f: #Writes to repost file that was unidentified
                f.write('root/'+file+" was unidentified and written to file "+os.getcwd()+'/'+unidentified_file+'\n')


#If there isn't directory for sample_id, it is made
def make_directories(sample_id, dest, report_name):
    os.mkdir(dest+'/'+sample_id) #Make new sampe_id-directory
    folder_items = parser.items("folders") #Gets all required folders from config-file
    for key, folder in folder_items: #Runs over every directory that is listed in confid-file's section folders
        os.mkdir(dest+'/'+sample_id+'/'+folder) #Makes subdirectory
    with open(report_name, 'a') as f: #Writes to report that directory and subdirectories were made.
        f.write("Created directory and subdirectories for sample_id '"+sample_id+"'\n")


def compare_files(newfile, oldfile, file_moved, report_name, dest, root): #Check md5sum of two files
    file1=newfile #
    file2=oldfile
    if os.path.islink(oldfile): #If oldfile was a symlink, to open and compare it program must compare files that are pointed by them
        file1=os.readlink(newfile) #For file comparison file that is pointed by new symlink
        file2=os.readlink(oldfile) #For file comparison file that is pointed by old symlink
    hash_md5_new = hashlib.md5() #Makes md5-number for new file
    with open(file1, "rb") as f: #Opens new file or file pointed by new symlink to count md5sum
        for chunk in iter(lambda: f.read(4096), b""): #Reads 4096 bits on a time to save memory
            hash_md5_new.update(chunk) #Updates md5sum with new bits

    hash_md5_old = hashlib.md5() #Makes md5-number for old file
    with open(file2, "rb") as f: #Opens old file or file pointed by old symlink to count md5sum
        for chunk in iter(lambda: f.read(4096), b""):  #Reads 4096 bits on a time to save memory
            hash_md5_old.update(chunk) #Updates md5sum with new bits
    if hash_md5_new.hexdigest()==hash_md5_old.hexdigest(): #Compares the md5sums if they are same
        if file_moved: #Checks if file was tried to move, or if file with same name already existed
            with open(report_name, 'a') as f: #Writes to report what file was moved and where.
                f.write("root/"+oldfile[len(root)+1:]+"\n---> dest/"+newfile[len(dest)+1:]+'\n') #Transfer is written to the report, without old root and destination-directory
    else: #If md5sums differ
        with open(report_name, 'a') as f:
            if file_moved: #If file was tried to copy
                f.write("Failed to copy file "+oldfile+" succesfylly. It differs from the destination file "+newfile+'\n')
                raise NameError('Original file\n'+Back.RED+oldfile+'\nand new file\n'+newfile+'\nDon\'t match. Something failed during copying.'+Back.RESET) #If they diffed, program raises error
            else: #If file wasn't copied because file with that name already existed, but that file differs from file that was about to be moved
                f.write("Failed to copy file "+oldfile+" because file with same name but different content already exists in the destination "+newfile+". ")
                raise NameError('Couldn\'t copy file \n'+Back.RED+oldfile+'\nBecause in the destination there already exists different file with the same name:\n'+newfile+Back.RESET) #If they diffed, program raises error


def checking_line_requirements(parameters, root, file_read, report_name, line): #Checks if line in unidentified-files.txt matches expectations
    if len(parameters)!=3: #Not right amount of commas, prints the line in red, writes about it to report and returns false so line is skipped
        print(Back.RED+"Error in file "+root+'/'+file_read+", there isn't right amount of commas in line "+line+Back.RESET)
        with open(report_name, 'a') as f:
            f.write("File "+root+'/'+file_read+" had wrong amount of commas in line "+line+'\n')
        return False
    if not os.path.isfile(parameters[1]): #File in that line doesn't exist, prints the line in red, writes about it to report and returns false so line is skipped
        print(Back.RED+"Error in file "+root+'/'+file_read+", couldn't find file named "+parameters[1]+Back.RESET)
        with open(report_name, 'a') as f:
            f.write("File "+root+'/'+file_read+" had non-existent filename in line "+line+'\n')
        return False
    if parameters[0]=="unknown" or parameters[2]=="XXX": #If directory or sample_id isn't still known, returns false and line is skipped
        return False
    return True #If everything was fine, returns True so file of the line can be moved


def delete_identified_lines(root, file_read, removable_lines, report_name): #Deletes identified files from unidentified-files.txt after they have been moved
    with open(root+'/'+"temp.txt", "w+") as fw: #Creates temporary.txt where lines that won't be deleted are written
        with open(root+'/'+file_read, "r+") as fr: #Opens original unidentified-files.txt
            for line in fr: #Goes old file over line by line
                if not line.strip("\n") in removable_lines: #If line is not supposed to be deleted it is written to temporary file
                    fw.write(line)
    os.remove(root+'/'+file_read) #Removes old version
    os.rename(root+'/'+"temp.txt",(root+'/'+file_read)) #Rename temporary file to original file name

    with open(report_name, 'a') as f: #Opens report to write which lines were removed, if any
        if(len(removable_lines)!=0): #If some lines were removed
            f.write("Removed lines\n")
            for line in removable_lines: #Writes every removed line
                f.write("'"+str(line)+"'\n") #Writes removed line with linebreak
            f.write("from file '"+file_read+"'\n\n")
        else: #If no lines were Removed
            f.write("There were no lines to be removed in file '"+file_read+"'\n\n")




def move_unidentified_files(root, file_read, dest, report_name): #Moves files that are written to unidentified-files.txt
    moved_files = list() #Record files that are moved using the text file, so they won't me touched later in the program

    with open(report_name, 'a') as f: #Writes to report that program is moving files from unidentified-files.txt
        f.write("Moving files in '"+file_read+"'.\n")

    with open(root+'/'+file_read, "r+") as f: #Opens unidentified-files.txt
        f_lines = f.readlines() #Saves all files lines to f_lines
        removable_lines=list() #Keep record of the lines that can be removed from text file later

        for line in f_lines: #Check unidentified-file line by line
            if '#' in line or line=="\n": #Headers and empty rows are ignored
                continue #Moves to next line

            line=line.strip("\n") #Removes linebreaks from lines, so sample_ids that are in the end of lines don't contain them.
            parameters=line.split(',') #Split three parameters from line (directory,/path/to/file,sample_id)
            if not checking_line_requirements(parameters, root, file_read, report_name, line): #Check if line does not meet the expectations
                continue #If it doesn't, program skips the line

            sample_id=parameters[2].strip() #Sample_id is the last of three parameters, strip removes all possible surrounding spaces
            root_parameters=parameters[1].split('/') #Splits the root (/path/to/file) to parameters, root is second parameter in row
            file=root_parameters[-1] #Gets file from last parameter
            pattern_root=re.compile(r'^.*/') #Roots-pattern, everything before the file
            matches = pattern_root.finditer(parameters[1]) #Finds everything before the file from second parameter.
            for match in matches: #To get root from match
                file_root =match.group(0)[:-1] #Remove the last /, it would hinder file processing later
            if parameters[0]==vcf_destination: #If directory is same as vcf-directory
                if move_vcf_file(file_root,file,dest,sample_id,report_name): #Check if file can be moved like vcf-file. If not, sample_id was None
                    removable_lines.append(line) #If file was moved, write line up so it can be deleted later.
                    moved_files.append(file) #Program ignores moved file if it meets this again
            else: #If destination wasn't vcf-directory
                if move_sample_id_file(file_root, file, sample_id, dest, report_name, parameters[0]): #Last parameter is the destination directory
                    removable_lines.append(line) #Write down line which will be deleted from file
                    moved_files.append(file) #Program ignores moved file if it meets this again
    delete_identified_lines(root, file_read, removable_lines, report_name) #Deletes all the lines whose files were moved.
    return moved_files #Returns all moved_files so program can ignore them later



def move_annotation_files(root, dest, files, report_name, ignored_files): #Moves all files that were in same directory with file "with_annotations"
    for file in files: #Check every file in annotation-directory
        if file in ignored_files: #Check if file is in ignored_files
            continue #File is in ignored_files, move to next one
        file_moved=False #Used later when old and destination files are compared, if there already existed file with same name in destination file_moved remains false
        sample_id=None #Keep count if sample_id is found

        pattern_patient=re.compile(r'\d{6}_.{6}_\d{4}_.{10}_.*_\w\d{3}_\w\d{3}') #Tries to find Epi-Ski-type sample_id
        matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
        for match in matches_sampleid: #Check if sample_id type 'Epi-Ski'
            sample_id = match.group(0)[30:len(match.group(0))-10] #Sample_id separated

        if sample_id==None: #If sample_id was not Epi-Ski, search for sample_if more widely
            pattern_patient2 = re.compile(r'^(S\d+(_\d+)?|SRR\d+|[A-Z]+_\d+|\d+_[A-Z]+)[._]') #Check for sample_id in the filename more widely
            matches_sampleid2 = pattern_patient2.finditer(file)
            for match in matches_sampleid2:
                sample_id = match.group(0)[0:len(match.group(0))-1] #Separates the sample_id from match

        if sample_id==None: #If sample_id wasn't still founded
            write_unidentified_file(annotation,root,file,sampe_id,report_name) #File is moved to unidentified_files
            break #Moves to next file

        if not os.path.isdir(dest+'/'+sample_id): #Check, if there already exists a directory for sample_id
            make_directories(sample_id,dest, report_name) #If not, nove directory is made

        if not os.path.isfile(dest+'/'+sample_id+'/'+annotation+'/'+file): #If file doesn't exist yet in new location
            shutil.copy(root+'/'+file, dest+'/'+sample_id+'/'+annotation+'/'+file, follow_symlinks=False) #Copy file to new destination
            file_moved=True #Important in compare_files-function, it knows that old file was copied
            compare_files(dest+'/'+sample_id+'/'+annotation+'/'+file, root+'/'+file, file_moved, report_name,dest,root)
        else: #If file with same name already exists
            if root==dest+'/'+sample_id+'/'+annotation: #If root and destination are same, same filed is being moved again
                break #Go to the next directory
            elif "with_annotations" in file: #If it is 'with_annotations'-file, it is still copied with timestamp
                pattern_prefix = re.compile(r'\.[^\.]*$') #Find the ending of the file
                matches = pattern_prefix.finditer(file) #Searches the pattern from filename
                for match in matches: #Checks if pattern was found
                    new_filename = file[:(len(file)-len(match.group(0)))]+datetime.datetime.now().strftime(".%Y%m%dT%H%M%S")+file[(len(file)-len(match.group(0))):] #Make new filename with timestamp just before ending
                shutil.copy(root+'/'+file, dest+'/'+sample_id+'/'+annotation+'/'+new_filename, follow_symlinks=False) #Copy file to new destination
                file_moved=True #Important in compare_files-function, it knows that old file was copied
                compare_files(dest+'/'+sample_id+'/'+annotation+'/'+new_filename, root+'/'+file, file_moved, report_name,dest,root)
                continue #Moves to next file
            compare_files(dest+'/'+sample_id+'/'+annotation+'/'+file, root+'/'+file, file_moved, report_name,dest,root) #If file already exists and it wasn't 'with_annotations', program checks if it matches



def move_log_file(root, file, log_file, dest, report_name): #Moves all log-files to same directory
    if not os.path.isdir(dest+'/'+log_folder): #Checks if there already exists directory for log-files
        os.mkdir(dest+'/'+log_folder) #If not, makes a new one
        with open(report_name, 'a') as f: #Opens report to write that new directory for log-files was made.
            f.write("Made directory '"+log_folder+"' to "+dest+'\n')
    x=1 #Running number that is being used to rename log-files
    new_filename=root.replace('/','_')[1:]+'_'+file[:(len(file)-len(log_file.group(0)))]+".{:02d}".format(x)+file[(len(file)-len(log_file.group(0))):] #New filename is made from root, current file name and running number, so old files aren't overwritten
    while os.path.isfile(dest+'/'+log_folder+'/'+new_filename): #Increase running number so long that file with same name doesn't exist. Thus, file is always copied even if it exists already.
        x+=1 #Increases running number
        new_filename=root.replace('/','_')[1:]+'_'+file[:(len(file)-len(log_file.group(0)))]+".{:02d}".format(x)+file[(len(file)-len(log_file.group(0))):]#New filename is made from root, current file name and running number

    shutil.copy(root+'/'+file, dest+'/'+log_folder+'/'+new_filename, follow_symlinks=False) #Copying, symlinks=false-> if file is symlink, this makes a new symlink to new location pointing to the original file, in stead of copying the real file from the destination of symlink pointer
    compare_files(dest+'/'+log_folder+'/'+new_filename, root+'/'+file, True, report_name,dest, root) #compare new and original file



def move_sample_id_file(root, file, sample_id, dest, report_name, vcf_file): #Moves files that contained sample_id and are located in directories listed in config-file
    if not os.path.isdir(dest+'/'+sample_id): #Check, if there already exists a directory for sample_id
        make_directories(sample_id,dest, report_name) #If not, makes new directories and subdirectories
    file_moved=False #So compared_files-function know if file was tried to move or if file with same name already existed in the destination

    path_items = parser.items("folders") #Section in config-file where directories are listed
    for key, folder in path_items: #Checks every folder in config-file
        if root.endswith('/'+folder) or vcf_file==folder: #If file's current folder is some folder from the list, or move_unidentified_files has called this function the folder can be found at vcf_file variable
            if not os.path.isfile(dest+'/'+sample_id+'/'+folder+'/'+file): #If file doesn't exist yet
                shutil.copy(root+'/'+file, dest+'/'+sample_id+'/'+folder+'/'+file, follow_symlinks=False) #Copying, symlinks=false-> if file is symlink, this makes a new symlink to new location pointing to the original file, in stead of copying the real file from the destination of symlink pointer
                file_moved=True #Marks that original file was copied
            compare_files(dest+'/'+sample_id+'/'+folder+'/'+file, root+'/'+file, file_moved, report_name,dest,root) #compare destination and original file, regardless of if file was copied or it existed in the destination already
            return True #Returns true so program knows that file was moved

    if vcf_file==False: #If current directory wasn't listed in config-file and file isn't vcf-file (which are moved to vcf-directory):
        write_unidentified_file(None, root, file, sample_id, report_name) #file is written to unidentified-files.txt
        return True #Returns true so program can move to next file

    return False #File couldn't yet be moved, but is a vcf-file


def find_vcf_sample_id(root, file, sample_id):
    with open(root+'/'+file, encoding="utf8", errors='ignore') as f: #Open file to search for a sample_id, utf8 so it can be read, ignores everything that can't be read
        contents=f.read()

        i=0
        pattern = re.compile(r'TUMOR,SampleName=[A-Z]+_?\d+') #First, let's try to find sample name from file with the most reliable way from file
        matches = pattern.finditer(contents) #Searches for pattern in file
        for match in matches: #Checks if there are any matches
            i=i+1 #If match was found, increases i. If many matches are found i>1
            if i>1: #If multiple matches are found, they are compared
                if match.group(0)[17:]!=sample_id: #Compares new match to the previous
                    return None #Returns that sample_id=None if two matches differentiate, because then sample_id can't be recognized
            sample_id = match.group(0)[17:] #Separates sample_id from new match

        if sample_id==None: #If sample_id still wasn't found from file
            pattern2 = re.compile(r'gatk/(S\d+(_\d+)?|SRR\d+|[A-Z]+_\d+|\d+_[A-Z]+)[_.]') #Second, program tries to find sample name from file with gatk/
            matches=pattern2.finditer(contents) #Searches for pattern in file
            for match in matches: #Checks if there are matches
                i=i+1 #If match was found, increases i. If many matches are found i>1
                if i>1: #If multiple matches are found, they are compared
                    if match.group(0)[17:]!=sample_id: #Compares new match to the previous
                        return None #Returns that sample_id=None if two matches differentiate, because then sample_id can't be recognized
                sample_id = match.group(0)[5:len(match.group(0))-1] #Separates sample_id from rest of the pattern
    return sample_id




def move_vcf_file(root, file, dest, sample_id, report_name): #Copies vcf-files
    file_moved=False #So compared_files-function know if file was tried to move or if file with same name already existed in the destination
    if sample_id==None: #If sample_id is not yet known, function searches it wider
        sample_id=find_vcf_sample_id(root,file,sample_id) #Tries to find sample_id with function find_vcf_sample_id

    if sample_id==None: #If program hasn't found sample_id, it writes file to unidentified
        write_unidentified_file(vcf_destination, root, file, None, report_name) #Writes file to unidentified without sample_id
        return #Returns so program can move to next file

    if not os.path.isdir(dest+'/'+sample_id): #If sample_id was found checks if there is already a directory for it
        make_directories(sample_id,dest, report_name) #Makes new directory for new sample_id
    if not os.path.isdir(dest+'/'+sample_id+'/'+vcf_destination): #Checks if there exists tumor-files-directory in sample_id's directory
        os.mkdir(dest+'/'+sample_id+'/'+vcf_destination) #Make tumor-files-directory
        with open(report_name, 'a') as f: #Opens report
            f.write("Created directory '"+vcf_destination+"' for sample_id '"+sample_id+"'\n") #Writes that tumor-directory was made

    if not os.path.isfile(dest+'/'+sample_id+'/'+vcf_destination+'/'+file): #Check, that same file isn't moved again, otherwise there would be error
        shutil.copy(root+'/'+file, dest+'/'+sample_id+'/'+vcf_destination+'/'+file, follow_symlinks=False) #Copy file to new location
        file_moved=True #So compared_files-function know if file was tried to move or if file with same name already existed in the destination
    compare_files(dest+'/'+sample_id+'/'+vcf_destination+'/'+file, root+'/'+file, file_moved, report_name, dest, root) #Compare new and original file
    return True



def check_if_annotation_dir(root, dest, files, report_name, ignored_files): #Checks if current directory contains is annotation-directory
    for file in files: #Check if there is "with_annotations"-file in directory. If there is, all files go to new annotation directorry. Also looks for unidentified.files.txt so it won't be mixed with other files
        if "with_annotations" in file: #Checks if file contains "with_annotations" in its name
            move_annotation_files(root, dest, files, report_name, ignored_files) #This is annotation directory so files are moved with move_annotation_files
            return True, ignored_files #Returns true so program can move to next directory, and files that can be ignored in the future
        if file==unidentified_file: #Checks if file unidentified-files.txt is in the directory
            #If file is unidentified-files.txt it moves file in it with move_unidentified_files
            ignored_files=ignored_files + move_unidentified_files(root, file, dest, report_name) #adds all moved files to ignored files so program can skip them later
            ignored_files.append(unidentified_file) #Ignore also unidentified_files.txt
    return False, ignored_files #Returns False if directory wasn't annotation-dir and ignored files



def move_file(file,root,dest, report_name): #Function to move files that weren't in annotation directory, forbidden symlinks or in ignored-list
    file_moved=False #So compared_files-function know if file was tried to move or if file with same name already existed in the destination
    sample_id=None #Keeps count if sample_id is found

    pattern_log = re.compile(r'\.(ER|job|OU|log)$') #Check if file is a log-file
    matches_log = pattern_log.finditer(file) #Searches for log-file-ending from file
    for log_file in matches_log: #Checks if there is log-ending in file
        move_log_file(root, file, log_file, dest, report_name) #File is a log-file, it is moved with move_log_file, returns always True
        return #move_log_file always moves the file, so program can continue to next file

    vcf_file=False #Keeps count if file is vcf-file or not
    pattern_vcf = re.compile(r'.*\.(vcf(\.idx)?|bcf)$') #Vcf-files endings in pattern
    matches_vcf = pattern_vcf.finditer(file) #Checks for vcf-file-ending from a filename
    for match in matches_vcf: #Checks if file had vcf-ending
        vcf_file=True #If it had, file is a vcf-file

    pattern_patient=re.compile(r'\d{6}_.{6}_\d{4}_.{10}_.*_\w\d{3}_\w\d{3}') #Epi-Ski-sample_id pattern
    matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename, type 'Epi-Ski'
    for match in matches_sampleid: #Checks if sample_id was found
        sample_id = match.group(0)[30:len(match.group(0))-10] #Sample_id separated from rest of the pattern
        if move_sample_id_file(root, file, sample_id, dest, report_name, vcf_file): #Case, that file isn't log-file but contains sample_id, tries to move file with move_sample_id-file
            return #Returns False if current folder didn't meet the expectations and file is a vcf-file. Otherwise program can continue to next file

    pattern_patient2 = re.compile(r'^(S\d+(_\d+)?|SRR\d+|[A-Z]+_\d+|\d+_[A-Z]+)[._]') #More vague pattern for sample_id
    matches_sampleid2 = pattern_patient2.finditer(file) #Check for sample_id in the filename more widely
    for match in matches_sampleid2: #Checks if sample_id was found
        sample_id = match.group(0)[0:len(match.group(0))-1] #Separates sample_id from rest of the pattern
        if move_sample_id_file(root, file, sample_id, dest, report_name, vcf_file): #Case, that file isn't log-file but contains sample_id, tries to move file with move_sample_id-file
            return #Returns False if current folder didn't meet the expectations and file is a vcf-file. Otherwise program can continue to next file
    #If file hasn't yet been moved
    if vcf_file: #If file is a tumorfile
        move_vcf_file(root, file, dest, sample_id, report_name) #If file is vcf-file it is moved with move_vcf_file():
        return #move_vcf_file always copies file so program can move to next line
    #Couldn't move the file, it is written to unidentified-files
    path_items = parser.items("folders") #Section where all the folders are listed
    for key, folder in path_items: #Checks every folder and compares them to current one. If there is a match, destination folder is known
        if root.endswith('/'+folder): #Checks if destination directory can be identified
            write_unidentified_file(folder, root, file,None,report_name) #Destination directory can be identified, only sample_id is unknown
            return #Moves to next file
    write_unidentified_file(None, root, file, None, report_name) #sample_id and directory are unknown



def directory_sorting(ignored_directories,ignored_files, starting_directory, dest, report_name): #Goes through every wanted directory and file
    ignored_directories.append(log_folder) #Ignore log_folder or all the files in it will be recopied
    for root, dirs, files in os.walk(starting_directory, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
        print(root) #Print current directory
        with open(report_name, 'a') as f: #Write current directory aka. root to report
            f.write("\nIn directory (root): "+root+'\n')

        if root[:-1]==dest: #If current directory is starting directory, there is one '/' too much in the end
            root=root[:-1] #Starting root has '/' in the end: makes things complicated
        dirs[:] = [d for d in dirs if d not in ignored_directories] #Delete ignored directories from the directories to be went through

        annotation_dir, ignored_files = check_if_annotation_dir(root, dest, files, report_name, ignored_files) #Check if current directory is annotation directory or if there is unidentified-files.txt
        if annotation_dir: #If current directory is annotation-directory, files have been moved
            continue #Program can move to the next directory
        #Directory wasn't annotation-dir or in ignored directories
        for file in files: #Go through all the files in the current directory
            if file in ignored_files or "file_arrangement_report" in file or not os.access(root+'/'+file, os.R_OK): #Check if file is supposed to be ignored, reports are untouched. Also checks user has access to read file so it can be copied.
                with open(report_name, 'a') as f: #Write current directory aka. root to report
                    f.write("Skipped file: '"+root+'/'+file+"'\n")
                continue #If file was in ignored_files, program moves to the next file

            move_file(file,root,dest, report_name) #We have permission to copy the file so it goes to further treatment

def send_email(email_address):
    pass
    #     currentDT = datetime.datetime.now()
    #     title="File_arrangement report "+currentDT.strftime("%Y-%m-%d %H:%M:%S")
    #     message="You can find report attached. If there was some unidentified files, file named \"unidentified_files.txt\" should be attached too."
    #     attach_to_message(os.getcwd()+'/'+"program_report.txt")
    #     if os.path.isfile(os.getcwd()+'/'+"unidentified_files.txt"):
    #         attach_to_message("unidentified_files.txt")
    #     sendmail
    #     print(Back.GREEN + 'Email sent to address '+values.mail+Back.RESET)

def check_optparsing(optparser, values): #Check if parsing arguments fulfil the requirements
    if values.src==None: #Check if starting directory was given
        optparser.error("Give directory to sort (-s /path/to/directory)") #Starting directory wasn't given, raises error
    if not os.path.isdir(values.src): #Check, if user made a spelling mistake in starting directory
        optparser.error("Directory "+values.src+" doesn't exist.") #User made a spelling mistake in starting directory, raises error
    if not os.path.isdir(values.dst): #Check, if user made a spelling mistake in destination directory
        optparser.error("Directory "+values.dst+" doesn't exist.") #User made a spelling mistake in destination directory, raises error

    if values.ign == None: #Check if user gave directories to be ignored
        ignored_directories=[] #If not, makes ignored directories to an empty list
    else: #User gave directories to be ignored
        ignored_directories = shlex.split(values.ign) #Separate multiple directories from each other
        for root, dirs, files in os.walk(values.src, topdown=True): #Check all the directories in starting directory to confirm that all given directories exist
            for dir in dirs:  #Check all the subdirectories
                if dir in ignored_directories: #If directory is in the ignored_directories
                    ignored_directories.remove(dir) #remove found directory from the list
        if len(ignored_directories)==1: #Check if there was a directory that couldn't be found
            optparser.error("Directory "+str(ignored_directories)+" doesn't exist.") #One directory didn't exist, program raises error
        elif len(ignored_directories)>1: #Check if there were many directories that couldn't be found
            optparser.error("Directories "+str(ignored_directories)+" don't exist.")  #Multiple directories didn't exist, program raises error
        else: #All given directories exist
            ignored_directories=shlex.split(values.ign) #Remake list of ignored_directories

    if values.file == None: #Check if user gave files to be ignored
        ignored_files=[] #If not, makes ignored files to an empty list
    else: #User gave files to be ignored
        ignored_files = shlex.split(values.file) #Separate multiple files from each other
        for root, dirs, files in os.walk(values.src, topdown=True): #Check all the directories in starting directory to confirm that all given files exist
            for file in files: #Check all the subdirectories
                if file in ignored_files: #If file is in the ignored_files
                    ignored_files.remove(file) #remove found file from the list
        if len(ignored_files)==1: #Check if there was a file that couldn't be found
            optparser.error("File "+str(ignored_files)+" doesn't exist.") #One file didn't exist, program raises error
        elif len(ignored_files)>1: #Check if there were many files that couldn't be found
            optparser.error("Files "+str(ignored_files)+" don't exist.") #Multiple files didn't exist, program raises error
        else: #All given files exist
            ignored_files=shlex.split(values.file) #Remake list of ignored_files

    return ignored_directories, ignored_files #Return separated and checked lists of ignored_directories and ignored_files

def optparsing():
    #Make parser header
    optparser = optparse.OptionParser(usage= "python3 %prog [command] [options]\n\
    In a given directory:\
    Moves log-files to log-directory without overrunning old files.\n\
    Makes sample_id directory for other files with sample_id and moves these there.\n\
    If there are files that can't be identified to neither of these, makes directory unidentified and moves them there.")
    #Add options to parser
    optparser.add_option("-s", "--source", dest="src", help="Directory to be copied (-s /path/to/directory)")
    optparser.add_option("-d", "--dest", dest="dst", default=os.getcwd(), help="Directory where sample directories are made (-d /path/to/directory). Default=current directory")
    optparser.add_option("-i", "--ignore", dest="ign", help="Directories to be ignored (-i \"dir1 dir2 dir3\")") #append? nargs?
    optparser.add_option("-f", "--file", dest="file", help="Files to be ignored (-f \"file1 file2 file3\")")
    optparser.add_option("-m", "--mail", dest="mail", help="If you want to receive a report via email after the program has run, write your email address")
    optparser.add_option("-u", "--unidentified", action="store_true", dest="operation", default=False, help="If you want to go through only the "+unidentified_file)
    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    ignored_directories, ignored_files = check_optparsing(optparser,values) #Check that parse_args fulfil requirements, returns two lists
    return values, ignored_directories, ignored_files

def main(): #Main contains mainly parser settings
    values, ignored_directories, ignored_files =optparsing()

    currentDT = datetime.datetime.now() #Get current datetime for report naming
    report_name, unidentified_files, ignored_files = make_files(values, currentDT, ignored_directories, ignored_files) #Make report and unidentified-files.txt if necessary

    if values.operation==True: #Check if user wants program run through only the unidentified.txt
        move_unidentified_files(values.src, unidentified_file, values.dst, report_name) #Go only through unidentified_files
    else: #Goes through every file in destination directory
        directory_sorting(ignored_directories, ignored_files, values.src, values.dst, report_name) #Program starts directory sorting

    if os.stat(os.getcwd()+'/'+unidentified_file).st_size == 649: #Check if there are any files in the unidentified-files.txt
        os.remove(os.getcwd()+'/'+unidentified_file)    #Remove empty file
        print(Back.GREEN + 'All files copied succesfully. Report is in '+values.dst+Back.RESET) #There were no unidentified files
        with open(report_name, 'a+') as f: #Write to report that all files were moved succesfully
            f.write("Removed empty file '"+unidentified_file+"'\n")
            f.write("All files copied succesfully.")
    else: #There are some files in unidentified-files.txt
        print(Back.GREEN + "Files copied succesfully, some unidentified files are located in "+unidentified_files+"."+Back.RESET)
        with open(report_name, 'a+') as f: #Write to report that all files were moved succesfully, except there are some in unidentified-files.txt
            f.write("Files copied succesfully, some unidentified files are located in '"+unidentified_files+"'.")
    if values.mail != None: #If user wants email
        send_email(values.mail)

    #No errors occured: program ran succesfully


if __name__ == '__main__': #If program was called directly
    start_time = time.time() #Starts clock
    main() #Starts main
    print (time.time() - start_time, "seconds") #Prints consumed time

    #Manuaalin kirjoitus loppuun
    #Onko kansioilla oikeat nimet
    #Sähköposti puuttuu
