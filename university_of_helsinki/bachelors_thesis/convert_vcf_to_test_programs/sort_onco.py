import optparse
import os
import re

def sort_file(values):
    with open(values.file, 'r') as fr:
        pattern=re.compile(r'/?[^/]*\.tsv')
        file="unknown"
        matches  = pattern.finditer(values.file)
        for match in matches:
            file=match.group(0)[:-4]
        with open(values.destination+'/'+file+'_sorted.tsv', 'w+') as fw:
            lines=fr.readlines()
            fw.write(lines[0])
            #for line in sorted(lines[1:], key=lambda line: (float(line.split()[2]), float(line.split()[3]), float(line.split()[1]))): #Sort by P-value
            for line in sorted(lines[1:], key=lambda line: (float(line.split()[2]), float(line.split()[1]), float(line.split()[3]))): #Sort by Q-value
                fw.write(line) #Write lines to sorted vcf, first they are sorted by chromosome then by position

def check_optparsing(values, optparser):
    if values.file==None and values.directory==None: #Checks that either file or directory is given
        optparser.error("Give file (-f /path/to/file) or directory (--directory /path/to/file)") #Raises error if not
    if values.file!=None and not os.path.isfile(values.file):
            raise NameError("Could not find file "+values.file+' from directory '+os.getcwd()+'.\n') #Raises error
    assert values.directory==None or os.path.isdir(values.directory), "Could not find given --directory"
    if not os.path.isdir(values.destination): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.destination+' from directory '+os.getcwd()+'.\n') #Directory was not found



def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [command] [directory name]\n\
    Sorts oncodrive output") #Make header for help page
    optparser.add_option("-f", "--file", dest="file", help="File to sort (-f /path/to/file)")
    optparser.add_option("--directory", dest="directory", help="If you want to sort whole directory")
    optparser.add_option("--destination", dest="destination", default=os.getcwd(), \
    help="destination to cdf file, report etc. (--destination /path/to/directory). Default is current directory")
    optparser.add_option("--identifier", dest="identifier", default="", help="Identifier for the correct files in the directory")
    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    check_optparsing(values, optparser)
    return values


def main():
    values=optparsing()
    if values.directory!=None:
        for root, dirs, files in os.walk(values.directory):
            for file in files:
                if not file.endswith(".tsv") or not values.identifier in file:
                    continue

                values.file=root+'/'+file
                #print(values.file, root+'/'+file)
                sort_file(values)
    else:
        sort_file(values)
    print("All files sorted succesfully, they can be found from directory '"+values.destination+"'.")

if __name__ == '__main__':
    main()
