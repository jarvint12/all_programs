from datetime import datetime
import collections


#Writes info to line
def write_info(bam_columns, f):
    f.write("DP="+bam_columns[3]) #Max depth?
    f.write("\t") #Separates with tab to the next column

#Writes format column to lines
def write_format(f, count_forward, count_reverse, bam_columns):
    f.write("GT:AD:ADF:ADR\t0/1:"+bam_columns[3]+':'+str(count_forward)+':'+str(count_reverse)+'\n') #Total depth, forward depth and reverse depth

#Saves and count all variant types on one mpileup line
def count_variant_types(bam_columns):
    variants=collections.Counter() #Makes counter for variants
    j=0 #Initialize j for + and - signs
    k=0 #Initialize k for length of + or - strings
    l=0 #Initialize l to count when string is as long as k
    my_list = ['A', 'C', 'G', 'T', 'N', '+', '-'] #Different type of variables
    for i in range(len(bam_columns[4])): #For there is characters in mpileup column
        char = bam_columns[4][i].upper() #Make all letters upper so it is easier to compare variants
        print(char)
        if j==1 and char.isdigit(): #If current character is number and there has been + or - sign before
            if k!=0: #If insertion/deletion is over 9
                k=10*k+int(char) #Multiple previous number by ten and add new number
            else: #It is the first number of insertion
                k=int(char) #K tells how many insertions or deletions there are
        elif char in my_list: #If character is in the variant list
            if char=='+' or char=='-': #If character is insertion or deletion
                j=1 #Keep count that current string is insertion or deletion
                string=char #Initialize string to that variable
                continue #Move to the next character
            elif j==1: #There is currently insertion or deletion
                string+=char #Add character to the string
                l+=1 #Increase l so it can be compared to the k
            else: #1 base has been vhanged
                variants[char] += 1 #Add base to the variables
        if j==1 and l==k: #If there has been a + sign and all insertions/deletions have been went through
            variants[string]+=1 #Add whole insertion/deletion variant to the string
            j=0 #Reinitialize j
            l=0 #Reinitialize l
            k=0
        print(variants)
    if j==1: #Last characters were insertion or deletion
        variants[string]+=1 #Add last string to variants
    return variants #Return collection containing all different variables and their amount

def write_given_variant(vcf_file, bam_columns, count_forward, count_reverse, bases):
    f= open(vcf_file, 'a') #Opens vcf file for appending
    for variant in bases:
        f.write(bam_columns[0]+'\t'+bam_columns[1]+'\t'+'.'+'\t'+bam_columns[2]+'\t'+variant+'\t.\t.\t') #Writes chromosome, position, id and reference base
        write_info(bam_columns, f) #Writes info column
        write_format(f, count_forward, count_reverse, bam_columns) #Writes format column
    f.close()
#Checks all variants in mpileup line and writes most common to the vcf
def variant_calling(vcf_file, bam_columns, count_forward, count_reverse):
    f= open(vcf_file, 'a') #Opens vcf file for appending
    f.write(bam_columns[0]+'\t'+bam_columns[1]+'\t'+'.'+'\t'+bam_columns[2]) #Writes chromosome, position, id and reference base
    variants = count_variant_types(bam_columns) #Counts all different variant types on line

    most_common=variants.most_common()[0][0] #Get the most common variable
    if most_common[0]=='+': #If most common was insertion
        f.write('\t'+bam_columns[2]+most_common[1:]) #Writes original base pair and insertion
    elif most_common[0]=='-': #If most common was a deletion
        f.write(most_common[1:]+'\t'+bam_columns[2]) #Writes deletion to the original base pair and current base pair
    else: #SNV
        f.write('\t'+most_common) #Writes variable

    f.write('\t.\t.\t') #Writes quality and filter columns
    write_info(bam_columns, f) #Writes info column
    write_format(f, count_forward, count_reverse, bam_columns) #Writes format column
    f.close() #Closes file


def make_vcf(new_vcf, reference):
    f=open(new_vcf, 'w+') #Creates new vcf-file
    date=datetime.now().strftime("%Y%m%d") #Datetime for header
    #Writes header (fileformat, filedate, reference file, Info fields nad oclumn headers)
    f.write('##fileformat=VCFv4.3\n##filedate='+date+'\n##reference=file:'+reference+'\n##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">\n')
    f.write('##FORMAT=<ID=AD,Number=1,Type=Integer,Description="Read depth for each allele">\n')
    f.write('##FORMAT=<ID=ADF,Number=1,Type=Integer,Description="Read depth for each allele on the forward strand">\n')
    f.write('##FORMAT=<ID=ADR,Number=1,Type=Integer,Description="Read depth for each allele on the reverse strand">\n')
    f.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    f.write('#CHROM POS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n')
    f.close() #Closes file


if __name__ == '__main__':
    make_vcf("new_vcf.vcf")
