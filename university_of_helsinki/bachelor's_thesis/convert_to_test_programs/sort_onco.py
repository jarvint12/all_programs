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
            i=0
            for line in lines:
                if line.startswith('#'):
                    fw.write(line)
                    i+=1
                else:
                    fw.write(line)
                    i+=1
                    break
            for line in sorted(lines[i:], key=lambda line: (float(line.split()[2]), float(line.split()[3]), float(line.split()[1]))): #Sort not header lines by chromosome
                fw.write(line) #Write lines to sorted vcf, first they are sorted by chromosome then by position

def check_optparsing(values, optparser):
    if values.file==None: #Checks that either file or directory is given
        optparser.error("Give file (-f /path/to/file)") #Raises error if not
    if not os.path.isfile(values.file):
            raise NameError("Could not find file "+values.file+' from directory '+os.getcwd()+'.\n') #Raises error
    if not os.path.isdir(values.destination): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.destination+' from directory '+os.getcwd()+'.\n') #Directory was not found



def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [command] [directory name]\n\
    Sorts oncodrive output") #Make header for help page
    optparser.add_option("-f", "--file", dest="file", help="File to sort (-f /path/to/file)")
    optparser.add_option("--destination", dest="destination", default=os.getcwd(), \
    help="destination to cdf file, report etc. (--destination /path/to/directory). Default is current directory")
    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    check_optparsing(values, optparser)
    return values


def main():
    values=optparsing()
    sort_file(values)


if __name__ == '__main__':
    main()
