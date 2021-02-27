import optparse
import collections


#COUNTS HOW MANY MUTATIONS IN ANNOTATION FILE

def count(values):
    f=open(values.file, 'r')
    lines=f.readlines()[1:]
    insertions=collections.Counter()
    deletions=collections.Counter()
    not_exonic=collections.Counter()
    synonymous=0
    nonsynonymous=0
    tot=0
    muut=0
    snv=0
    eri=0
    koko=0
    insertit2=collections.Counter()
    deli2=collections.Counter()
    for line in lines:
        if line.startswith('#'):
            continue
        koko+=1
        columns=line.split()
        if len(columns[3])>1 or columns[4]=='-':
            #if len(columns[3])==1:
            #    print(line)
            deletions[len(columns[3])]+=1
            deli2[len(columns[3]),columns[5]]+=1
            tot+=1
        elif len(columns[4])>1 or columns[3]=='-':
            insertions[len(columns[4])]+=1
            insertit2[len(columns[4]), columns[5]]+=1
            #if len(columns[4])==119:
                #print(line)
            tot+=1
        else:
            if columns[5]=="exonic":
                if columns[8]=="synonymous":
                    synonymous+=1
                    tot+=1
                    snv+=1
                elif columns[8]=="nonsynonymous":
                    nonsynonymous+=1
                    tot+=1
                    snv+=1
                else:
                    not_exonic[columns[8]]+=1
                    tot+=1
            else:
                not_exonic[columns[5]]+=1
                muut+=1
                tot+=1
    print(tot, snv, deletions, insertions, synonymous, nonsynonymous, not_exonic, muut, eri, koko, insertit2, deli2)

def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [command] [directory name]\n\
    Count mutations in annotated file") #Make header for help page
    optparser.add_option("-f", "--file", dest="file", help="File to analyze (-f /path/to/file)")
    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    if values.file==None: #Checks that either file or directory is given
        optparser.error("Give file (-f /path/to/file)") #Raises error if not
    return values

def main():
    values=optparsing()
    count(values)

main()







#
# 8829 1284
# Counter({1: 1202, 2: 959, 4: 629, 3: 557, 5: 171, 6: 152, 8: 106, 10: 80, 12: 73, 7: 48, 14: 44, 9: 42, 16: 31, 15: 25, 11: 24, 13: 18, 22: 17, 17: 16, 20: 16, 18: 14, 19: 9, 24: 9, 23: 9, 21: 6, 25: 5, 28: 4, 26: 3, 29: 3, 34: 3, 32: 3, 60: 2, 27: 2, 30: 2, 33: 2, 31: 2, 39: 2, 49: 1, 40: 1, 35: 1, 43: 1, 37: 1, 69: 1, 55: 1, 202: 1})
# Counter({1: 1049, 2: 612, 4: 440, 3: 355, 5: 138, 6: 128, 8: 102, 12: 60, 7: 55, 10: 55, 9: 51, 11: 22, 15: 21, 16: 20, 14: 20, 13: 17, 19: 12, 18: 11, 20: 11, 21: 8, 22: 8, 27: 6, 23: 5, 24: 5, 25: 5, 26: 4, 17: 4, 30: 2, 40: 2, 31: 2, 36: 2, 74: 1, 33: 1, 28: 1, 29: 1, 45: 1, 39: 1, 42: 1, 59: 1, 41: 1, 57: 1, 51: 1, 61: 1, 46: 1, 32: 1, 120: 1})
# 745 539
# Counter({'intergenic': 24707, 'intronic': 18630, 'ncRNA_intronic': 2639, 'UTR3': 1447, 'downstream': 507, 'ncRNA_exonic': 506, 'upstream': 498, 'UTR5': 338, 'upstream;downstream': 37, 'splicing': 8, 'ncRNA_splicing': 1})
# 49318
