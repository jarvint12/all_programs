import subprocess
import os
import time
from datetime import datetime
import collections
import optparse
import re
import csv
import random
from pympler import asizeof

import make_vcf_file
import patient_name
import configparser

parser=configparser.ConfigParser()
parser.read('/csc/mustjoki2/variant_move/epi_ski/hus_hematology/Timo/bachelor_thesis/mutation_permutation_tool/mutation_load_config_atlas.ini') #Read config-file
samtools_location = parser.get('tools_and_envs','samtools') #Location for samtools
bedtools_location = parser.get('tools_and_envs','bedtools') #Location for bedtools
r_env = parser.get('tools_and_envs','r_env') #Location for r environment

#Makes program report
def make_report(values):
    currentDT=datetime.now()
    report = "reads_covering_sites_report_"+currentDT.strftime("%Y%m%dT%H%M%S")+".txt" #Report name with timestamp
    report_name=values.destination+'/'+report #Report with path so it can easily be opened later
    with open(report_name, 'w+') as f: #Makes report and writes header
        f.write(os.path.basename(__file__)+" report, "+currentDT.strftime("%Y-%m-%d %H:%M:%S")+".\n") #Writes report introduction
        if values.ignore!='0': #If there are flags set to ignore, it is written to report
            f.write("Ignored positions with bitflags "+values.ignore+'.\n') #Writes ignored flags to report
        if values.include!=' ': #If there are flags that should be included
            f.write("Counted only positions with bitflags "+values.include+'.\n') #Writes ignored flags to report
        if values.number==None: #If reference number was not given, CDF was counted
            f.write("Counted CDF from largest to smallest: "+str(values.reverse)+'.\nIntervals of the prints are min '+str(values.percent)+'%.\n') #Writes, if CDF was counted from largest to smallest or not and the interval
        else: #If reference number was given
            f.write("Counted CDF only for given number "+str(values.number)+'.\n') #Writes that CDF was counted only for given number
            f.write("Counted how many genomic positions had more (True) or less (False) reads than given number: "+str(values.more)+'.\n') #Writes, whetever number of reads exceed or underspend given reference number
        f.write("Limit is "+str(values.limit)+'\n') #Write given limit
        f.write("Counted average of numbers below the limit: "+str(values.lower)+'.\n') #Write, if average was counted below or above of limit
        if values.head!='': #If head argument was given
            f.write("Used argument head -n "+values.head+'.\n') #Writes used argument
        if values.bed!='': #Checks if bed-file was given
            f.write("Used bedfile "+values.bed+'.\n') #Writes used bed-file
        if values.other_args!='': #Check if there were some other arguments given for samtools view
            f.write("Other samtools arguments used: "+values.other_args+'.\n') #Writes other samtools arguments used

    return report_name #Returns report name for further use

#Writes CDF-fucntion to report
def write_report_cdf(report,percent,word,current_number, tot_count):
    with open(report, 'a') as f: #Opens reads covering sites report
        if percent==0: #If it is first time that function is called
            f.write('\n') #Adds a line break
        if current_number==-1: #If current_number is still initialized number
            f.write("0 genomic positions with given requirements found.\n") #Writes that no genomic position with given requirements was found
            return
        if percent==101: #Program has gone through all lines
            f.write("100% of "+str(tot_count)+" genomic positions have "+str(current_number)+" or "+word+" reads covering site.\n") #Write last number to CDF-function
            return
        if percent==0 and current_number==1 and word=="less": #There is no numbers between 0 and 1, so it would be stupid to write "There are no numbers below 1 but greater than 0"
            return

        if percent==0: #If current number is first one and larger than 1 (different formatting if number is 1 and function goes upwards in numbers)
            f.write("0%  of genomic positions have "+word+" than "+current_number+" reads covering site.\n") #Write how many percent has only 1 read
        elif current_number==1 and word=="less": #If current number is 1 and program is going upwards, 1 must be the first number when occuring. Percent is already changed.
            f.write('{:.2f}'.format(100*percent)+"% ("+str(tot_count)+" pcs.) of genomic positions have 1 read covering site.\n") #Write how many percent has only 1 read
        else: #Current number is not the first one
            f.write('{:.2f}'.format(100*percent)+"% ("+str(tot_count)+" pcs.) of genomic positions have "+str(current_number)+" reads or "+word+" covering site.\n") #Writes how many percent and amount of genomic positions with reads more or less than current number


def annotate_vcf(values, generated_vcf_file, recursion_counter, f_report):
    i=0
    j=0
    headers=[]
    annotated_vcf=[]
    with open(generated_vcf_file, 'r') as f_generated:
        all_lines=f_generated.readlines()
        number_of_lines=len(all_lines)
        while(i<number_of_lines): #Create as many annotation files as necessary, reduces memory usage
            if all_lines[i].startswith('#'): #Goes through every header file and appends them to header string
                headers.append(all_lines[i])
                i+=1
                continue
            lines_to_write=headers+all_lines[i:min(number_of_lines-1, i+36693549)] #66693549, each file consist of the same header and then own variants
            i+=min(number_of_lines-1, i+36693549)
            with open(values.destination+"/new.vcf", 'w+') as fw:
                for line in lines_to_write:
                    fw.write(line)
            while not os.path.isfile(values.destination+"/temp_mutation_load"+str(j)+".hg38_multianno.txt"):
                os.system("rm "+values.destination+"/*.avinput "+values.destination+"/*refGene.* ")
                time.sleep(1)
                recursion_counter+=1
                if recursion_counter>1:
                    print("Uudestaan")
                    f_report.write("uusiks\n")
                os.system('time '+values.table_annovar+' '+values.destination+'/new.vcf \
                '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene -operation g -out '+values.destination+'/temp_mutation_load'+str(j))
                print('time '+values.table_annovar+' '+values.destination+'/new.vcf \
                '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene -operation g -out '+values.destination+'/temp_mutation_load'+str(j))
            if recursion_counter>1:
                print("Rekursio toteutettiin",recursion_counter,"kertaa")
                f_report.write("Recursion was done "+str(recursion_counter)+" times.\n")
            annotated_vcf.append(values.destination+"/temp_mutation_load"+str(j)+".hg38_multianno.txt")
            os.system("rm "+values.destination+"/new.vcf "+values.destination+"/temp_mutation_load"+str(j)+".hg38_multianno.vcf")
            time.sleep(1)
            j+=1
    with open(values.destination+"/temp_mutation_load.hg38_multianno.txt", "w+") as fw:
        i=0
        for file in annotated_vcf:
            with open(file, 'r') as f_r:
                lines=f_r.readlines()
                for line in lines[i:]:
                    fw.write(line)
            os.system("rm "+file)
            i=1

    return values.destination+"/temp_mutation_load.hg38_multianno.txt"

#Counts different type of variants from given vcf-files
def count_vcf_mutations(values,vcf_files, amount_of_files):
    snv, tot_sum, synonymous, nonsynonymous= (collections.Counter() for i in range(4))
    not_exonic, dels, insertions={},{},{}
    for i in range(amount_of_files):
        dels[i], insertions[i],not_exonic[i]= (collections.Counter() for i in range(3))
    for file in vcf_files: #Goes through every vcf file, annotates them and counts mutations and their types, categorizing them for random bam-file
        print('time '+values.table_annovar+' '+file+' \
        '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene -operation g -out '+values.destination+'/temp_mutation_load_ref_vcf')
        while not os.path.isfile(values.destination+'/temp_mutation_load_ref_vcf.hg38_multianno.txt'):
            os.system("rm "+values.destination+'/temp_mutation_load_ref_vcf*')
            os.system('time '+values.table_annovar+' '+file+' \
            '+values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene -operation g -out '+values.destination+'/temp_mutation_load_ref_vcf')
        f_anno=open(values.destination+'/temp_mutation_load_ref_vcf.hg38_multianno.txt', 'r')
        next(f_anno) #Skips header
        for line in f_anno: #Reads stdout line by line
            components = line.split() #Decodes line values and separate them
            if components[5]!="exonic" and values.skip_nonexon:
                continue
            file_number=random.randint(0,amount_of_files-1)
            if len(components[3])>1 or components[4]=='-': #If variant is deletion
                dels[file_number][len(components[3]),components[5]]+=1 #Add deletion's length, original base has already been removed
            elif len(components[4])>1 or components[3]=='-': #If variant is insertion
                insertions[file_number][len(components[4]),components[5]]+=1 #Add insertion's length, original base has already been removed
            else:
                if components[5]!="exonic" and values.intergenic:
                    not_exonic[file_number][components[5]]+=1
                elif values.separate_syn:
                    if components[5]!="exonic":
                        continue
                    if components[8]== 'synonymous':
                        synonymous[file_number]+=1
                    elif components[8] == 'nonsynonymous':
                        nonsynonymous[file_number]+=1
                    else:
                        not_exonic[file_number][components[8]]+=1
                snv[file_number]+=1 #Add snv to sum
            tot_sum[file_number]+=1 #Total sum of variants increases by one
        if not values.keep_anno:
            os.system("rm "+values.destination+"/temp_mutation_load_ref_vcf*")
        f_anno.close()
    print("Sizes:",asizeof.asizeof(tot_sum)//1024//1024//1024,asizeof.asizeof(snv)//1024//1024//1024,asizeof.asizeof(dels)//1024//1024//1024,\
    asizeof.asizeof(insertions)//1024//1024//1024,asizeof.asizeof(synonymous)//1024//1024//1024, asizeof.asizeof(nonsynonymous)//1024//1024//1024, asizeof.asizeof(not_exonic)//1024//1024//1024)
    return tot_sum, snv, dels, insertions, synonymous, nonsynonymous, not_exonic #Returns sums


def sample_lines_from_vcf(annotated_vcf_file, tot_sum):
    with open (annotated_vcf_file, 'r') as f_anno: #Opens coverages file for reading
        next(f_anno) #Skip header
        lines=f_anno.readlines()#Reads lines from annotated  generated vcf file
        print("Size of lines:",asizeof.asizeof(lines)//1024//1024//1024)
        if tot_sum>len(lines): #If there is not enough lines
            raise NameError("Not enough lines,"+str(tot_sum)+' > '+str(len(lines))+'.\n') #Raises error and leaves
        return lines #Gets randomly same amount lines as there are variants. Lines are in a random order


def permutate_snv_mutation(values,columns,written_not_exonic,not_exonic, written_nonsynonymous, nonsynonymous, written_synonymous, synonymous):
    if columns[5]!="exonic" and values.intergenic:
        if written_not_exonic[columns[5]]<not_exonic[columns[5]]:
            written_not_exonic[columns[5]]+=1
        else:
            return None, written_not_exonic, written_nonsynonymous, written_synonymous, written_not_exonic
    elif values.separate_syn:
        if columns[5]!="exonic":
            return None, written_not_exonic, written_nonsynonymous, written_synonymous, written_not_exonic
        if columns[8]=="nonsynonymous" and written_nonsynonymous<nonsynonymous:
            written_nonsynonymous+=1
        elif columns[8]=="synonymous" and written_synonymous<synonymous:
            written_synonymous+=1
        elif written_not_exonic[columns[8]]<not_exonic[columns[8]]:
            written_not_exonic[columns[8]]+=1
        else:
            return None, written_not_exonic, written_nonsynonymous, written_synonymous, written_not_exonic
    return columns[4], written_not_exonic, written_nonsynonymous, written_synonymous, written_not_exonic

#Creates new vcf and writes random variants based on above variant sums and coverages file
def write_permutated_vcf(values, annotated_vcf_file, vcf_file, tot_sum, snv, dels, insertions, synonymous, nonsynonymous, not_exonic,lines_of_annotated_vcf):
    lines=random.sample(lines_of_annotated_vcf,len(lines_of_annotated_vcf))
    written_deletion, written_insertions, written_not_exonic= (collections.Counter() for i in range(3))
    written_snv=written_synonymous=written_nonsynonymous=written_sum=0 #Initializes sum for written SNV
    f_vcf = open(vcf_file,'a') #Opens vcf file for appending
    bases=['A','T','C','G'] #Different possible bases
    for line in lines: #Goes randomly sampled lines through
        columns=line.split() #Gets columns from coverages file line
        variant=None #Initializes variant to None so program knows if it is already changed
        if written_snv<snv: #If there is not yet enough SNV lines
            variant, written_not_exonic, written_nonsynonymous, written_synonymous, written_not_exonic= permutate_snv_mutation(values,columns,written_not_exonic,not_exonic, written_nonsynonymous, nonsynonymous, written_synonymous, synonymous)
            if variant!=None:
                written_snv+=1 #Add created variant to SNV sum
        if variant==None: #When all SNVs are written
            for deletion in dels: #Goes through every sized deletions
                if deletion[1]!=columns[5]: #Different area, deletion is type [length, area]
                    continue
                elif dels[deletion]>written_deletion[deletion]: #If all that sized deletions are not yet written
                    variant_list=random.choices(bases,k=deletion[0]) #Randomly samples bases, k is deletion size
                    variant=columns[3] #Variant is only the reference base
                    columns[3]=columns[3]+''.join(variant_list) #Add deletion to reference base
                    written_deletion[deletion]+=1 #Add one to written deletions on that sized deletion
                    break #Don't go bigger deletions through
        if variant==None: #All SNVs and deletions have been gone through, create insertion lines
            for insertion in insertions: #Go through different sized insertions
                if deletion[1]!=columns[5]: #Different area, insertion is type [length, area]
                    continue
                elif insertions[insertion]>written_insertions[insertion]: #If there isn't yet created enough that sized insertions
                    variant_list=random.choices(bases,k=insertion[0]) #Randomly samples bases, k is insertion size minus reference base
                    variant=columns[3]+''.join(variant_list) #Add insertion to reference base to variant position
                    written_insertions[insertion]+=1 #Add one to written insertions on that sized insertions
                    break #Don't go through bigger insertions
        if variant==None:
            continue
        written_sum+=1
        f_vcf.write(columns[0]+'\t'+columns[1]+'\t.\t'+columns[3]+'\t'+variant+'\t.\t.\t.\tGT\t0/1\n') #Write to vcf file
        if written_sum==tot_sum: #If All variant types have been gone through but there are still lines left (total sum is bigger than variant sums)
            break
    print(tot_sum, written_sum,snv, written_snv, dels, written_deletion, insertions, written_insertions, synonymous, written_synonymous, nonsynonymous, written_nonsynonymous, not_exonic, written_not_exonic)
    f_vcf.close() #Close vcf file

#Sorts vcf file by chromosome and position
def sort_permutated_vcf(values,vcf_file):
    vcf_sorted=open(values.destination+"/sorted_temp.vcf", 'w+') #Create new vcf file where lines are sorted
    vcf_orig=open(vcf_file,'r') #Open originally created vcf file for reading
    not_header=list() #Create list for not header lines
    for line in vcf_orig: #Go original vcf file line by line
        if line.startswith('#'): #If line is a header
            vcf_sorted.write(line) #Write line to new sorted vcf
        else: #Line is not header, it must be sorted
            not_header.append(line) #Add line to not headers list
    for line in sorted(not_header, key=lambda line: (int(line.split()[0]) if line.split()[0].isdigit() else 999, line.split()[0], int(line.split()[1]))): #Sort not header lines by chromosome
        vcf_sorted.write(line) #Write lines to sorted vcf, first they are sorted by chromosome then by position
    vcf_sorted.close() #Close sorted vcf
    vcf_orig.close() #Close original vcf-file
    os.remove(vcf_file) #Remove unsorted vcf
    os.rename(values.destination+"/sorted_temp.vcf", vcf_file) #Rename sorted vcf file



#Takes vcf files as argument, counts their SNVs and insertions, takes as many lines from made coverages file as there are variants and makes SNVs and insertions same amount randomly
#as in the original vcf file
def permutate_vcf(values, generated_vcf_files, report):
    vcf_files=values.vcf_file.split() #Separates vcf files, doesn't matter if only 1 exists
    f_report=open(report, "a")
    if len(generated_vcf_files)==0:
        raise NameError("There are no generated vcf files.\n") #Raises error
    if len(vcf_files)!=len(generated_vcf_files):
        raise NameError("There is a different amount of original and generated vcf files. Probably not wanted.\n")
        tot_sum, snv, dels, insertions, synonymous, nonsynonymous, not_exonic = count_vcf_mutations(values,vcf_files, len(generated_vcf_files)) #Sum of different variant types
        if len(generated_vcf_files)==1:
            new_vcf_file=values.destination+"/"+patient_name.main(generated_vcf_files[0])+"_permutated"+datetime.now().strftime("%Y%m%dT%H%M%S")+".vcf" #Name of the new vcf-file
        else:
            new_vcf_file=values.destination+"/permutated_vcf"+datetime.now().strftime("%Y%m%dT%H%M%S")+".vcf" #Name of the new vcf-file
        make_vcf_file.make_vcf(new_vcf_file, values.reference) #Creates new vcf file name
        i=0 #Index for file numbers in write_permutated_vcf
        for generated_vcf_file in generated_vcf_files:
            annotated_vcf=annotate_vcf(values, generated_vcf_file, 0, f_report)
            write_permutated_vcf(values, annotated_vcf, new_vcf_file,tot_sum[i], snv[i], dels[i], insertions[i], synonymous[i], nonsynonymous[i], not_exonic[i],lines_of_annotated_vcf) #Creates new vcf and writes random variants based on above variant sums and coverages file
            i+=1 #Move to the next file
            if not values.keep_anno:
                os.system("rm "+values.destination+"/temp_mutation_load*")
                time.sleep(1)
        sort_permutated_vcf(values, new_vcf_file) #Sort new vcf file
    else:
        for vcf_file, generated_vcf_file in zip(vcf_files, generated_vcf_files):
            f_report.write("Permutating vcf_file "+vcf_file+" from generated vcf file "+generated_vcf_file+'\n')
            tot_sum, snv, dels, insertions, synonymous, nonsynonymous, not_exonic = count_vcf_mutations(values,[vcf_file], 1) #Sum of different variant types
            print("COUNTED")
            annotated_vcf=annotate_vcf(values, generated_vcf_file,0, f_report)
            lines_of_annotated_vcf=sample_lines_from_vcf(annotated_vcf, tot_sum[0])
            if values.perm_amount>1:
                if not os.path.isdir(values.destination+"/"+patient_name.main(generated_vcf_file)+"_permutations"):
                    os.mkdir(values.destination+"/"+patient_name.main(generated_vcf_file)+"_permutations")
            for i in range(values.perm_amount):
                if values.perm_amount>1:
                    new_vcf_file=values.destination+"/"+patient_name.main(generated_vcf_file)+"_permutations/"+patient_name.main(generated_vcf_file)+"_permutated_"+str(i)+".vcf"
                else:
                    new_vcf_file=values.destination+"/"+patient_name.main(generated_vcf_file)+"_permutated_"+str(i)+datetime.now().strftime("_%Y%m%dT%H%M%S")+".vcf" #Name of the new vcf-file
                make_vcf_file.make_vcf(new_vcf_file, values.reference) #Creates new vcf file name
                write_permutated_vcf(values, annotated_vcf, new_vcf_file, tot_sum[0], snv[0], dels[0], insertions[0], synonymous[0], nonsynonymous[0], not_exonic[0],lines_of_annotated_vcf) #Creates new vcf and writes random variants based on above variant sums and coverages file
                sort_permutated_vcf(values, new_vcf_file) #Sort new vcf file
            if not values.keep_anno:
                os.system("rm "+values.destination+"/temp_mutation_load*")
                time.sleep(1)
    f_report.close()


#User has given number argument, so only one number is compared to others
def compare_one_number(file, numbers_tot, count, more, number, report):
    percent=0
    tot_count=0
    while bool(count): #While there exists numbers is collections
        current_number=int(min(count.items(), key=lambda x: x[0])[0]) #Get the smallest number from the collection
        if more and current_number<number or not more and current_number>number: #Check if current number does not fulfil requirements
            del count[current_number] #Number did not fulfil the requirements so it is deleted
            continue #Program moves to the next number
        amount_of_number=int(min(count.items(), key=lambda x: x[0])[1]) #Number matched to the requirements, its amount is the second element from the collection
        tot_count+=amount_of_number #Add amount of the number to the total count
        percent+=amount_of_number/numbers_tot #Add percent of the number compared to the total amount of numbers to the total percent of numbers fulfilling requirements
        del count[current_number] #Delete counted number, moves to the next one

    if more: #If user wants to know how many numbers exceed the given number
        word="more" #Word written to the report is "more"
    else: #User wants to know how many numbers are smaller than given one
        word="less" #Word written to the report is "less"
    with open(report, 'a') as f: #Writes result to the report
        #Writes how many and what percent of positions have more or less than given number of reads covering site.
        f.write('{:.2f}'.format(100*percent)+"% ("+str(tot_count)+" pcs.) of "+str(numbers_tot)+" genomic positions have "+word+" than "+str(number)+" reads covering site.\n")


def config_intervals(number):
    intervals = parser.items("legend_intervals") #Gets all intervals from config-file
    last_interval=0 #Initializes last interval
    for key, interval in intervals: #Runs over all the intervals in the config file
        if number<int(interval): #if number is smaller than the interval
            break #Breaks so last_interval is the last number is greater or equal to
        else: #Number is greater or equal
            last_interval=interval #Save current interval to the las
    return last_interval #Return last interval that number was greater or equal to

#Counts the CDF function of given file
def cdf_function(file, numbers_tot, count, reverse, interval, report, writer, fnames, genome_size):
    percent=0 #Count cumulative percent for number of lines
    percent_printed=0 #Keep count what was the last percent that was printed
    tot_count=0 #Keep count of numbers that have been run through
    tot_sum=sum(count.values()) #Sum of total mapped reads
    current_number=-1 #Initialize current number, so program knows if there was not any in the collection
    word="less" #Initialize word
    sample_id=patient_name.main(file)
    while bool(count): #Goes through every number in the collection
        if reverse: #If user wants CDF-function to be counted from largest to smallest
            current_number=int(max(count.items(), key=lambda x: x[0])[0]) #Current number is the largest one from the collection
            amount_of_number=int(max(count.items(), key=lambda x: x[0])[1]) #Amount of that largest number
            word = "more" #Word used in reverse order is "more"
        else: #User wants to CDF-function from smallest to largest
            current_number=int(min(count.items(), key=lambda x: x[0])[0]) #Current number is the smallest one from the collection
            amount_of_number=int(min(count.items(), key=lambda x: x[0])[1]) #Amount of that smallest number
        if percent==0: #If current number is the first one
            write_report_cdf(report,percent,word,current_number, tot_count) #Writes report with 0 percent, current number already differs from -1
        tot_count+=amount_of_number #Add amount of current number to the total count
        plot_interval=config_intervals(current_number)
        writer.writerow({fnames[0]: sample_id, fnames[1] : current_number, fnames[2]: amount_of_number, fnames[3]: tot_count, fnames[4]: amount_of_number/genome_size, \
        fnames[5]: plot_interval})
        percent+=amount_of_number/numbers_tot #Add percent of the current number to the total percent
        if 100*(percent-percent_printed) >= interval: #If the difference between lastly printed and current percent differs more than given interval
            write_report_cdf(report,percent,word,current_number, tot_count) #Writes report with that interval
            percent_printed=percent #Change lastly printed percent
        del count[current_number] #Delete current number from collection and move to the next one

    if current_number==-1: #There were no numbers in the collection
        write_report_cdf(report,percent,word,current_number, tot_count) #Make a note to the report
        print("0 genomic positions with given requirements found.") #Inform user
    else: #There were numbers in the collection
        write_report_cdf(report,101,word,current_number, tot_count) #Write to the report that  all numbers have been went through. 101 percent can't be achieved otherwise

#Writes how many genomic positions had less than limit reads covering site and and average of numbers more or less than given limit
def write_report_averages_and_limits(report, limit, undersized_count, numbers_tot, tot_average_count, tot_average_sum, lower):
    if lower: #If user wants to know average of numbers less than given limit
        word="less" #Word used is less
    else: #User wants to know average of numbers more than given limit
        word="more" #Word is more

    with open(report, 'a') as f: #Opens program report
        if limit>1: #There are no reads less than 1 but more than 0, so check that limit is more than 1
            f.write(str(undersized_count)+" ("+'{:.2f}'.format(100*(undersized_count/numbers_tot))+'%) genomic positions had more than zero '+\
            'but less than '+str(limit)+' reads covering site.\n')#Writes how many positions had 0<reads<limit
        if tot_average_count>0: #If there were numbers found that are more or less than given limit
            f.write("Average of reads "+word+" than "+str(limit)+" is "+'{:.2f}'.format(tot_average_sum/tot_average_count)+".\n") #Writes average to the report
        else: #There were no reads more or less than limit
            f.write("Average of reads "+word+" than "+str(limit)+" is 0.\n") #Writes that average was 0


#Counts the length of whole reference genome
def whole_genome_length(file):
    stream = subprocess.Popen((samtools_location+' view -h '+file), \
      shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #Views file with header and captures output to stream
    sum=0 #Initialize sum of the length
    for line in stream.stdout: #Go output line by line
        values = line.decode('utf-8').split() #Split columns on line and decode it
        if values[0][0]!='@': #If value does not start with '@', header has ended and counting can be stopped
            break #Ends stream
        if values[0]!="@SQ": #If value does not specify sequence dictionary
            continue #Moves to the next line
        sum+=int(values[2][3:]) #Gets reference sequence length and sums is to total length
    return sum #Returns total length 3099750718


#Counts length of the area covered by merged final BED file
def bed_genome_length(bed_file):
    tot_length=0
    with open(bed_file, 'r') as fr:
        for line in fr:
            columns=line.split()
            if len(columns)<3:
                print("COLUMN LENS:",len(columns),columns)
                continue
            length=int(columns[2])-int(columns[1]) #0-based start 0A1A2T3C, 1-based end G=8, T=9, T=10...
            tot_length+=length
    return tot_length

#Write lines that have enough depth, and if there is enough variants also write vcf_file.
def write_coverages_and_vcf_files(components, f_cov, f_vcf, values): # Components=mpileup line columns
    count_forward = len(re.findall('[.ACGTN>*]', components[4])) #Count forward depth
    count_reverse = len(re.findall('[,acgtn<#]', components[4])) #Count reverse depth
    bases=['A', 'C', 'G', 'T']
    if components[2] not in bases:
        return
    else:
        bases.remove(components[2])
        if count_forward>=values.for_limit and count_reverse>=values.rev_limit and int(components[3])>=values.depth_lim: #If forward, reverse and total depths are enough
            f_cov.write(components[0]+'\t'+components[1]+'\t\t'+components[2]+'\t\t'+components[3]+'\t\t'+str(count_forward)+'\t\t'+str(count_reverse)+'\n') #Write to coverages file
            if f_vcf!=None:
                for variant in bases:
                    f_vcf.write(components[0]+'\t'+components[1]+'\t'+'.'+'\t'+components[2]+'\t'+variant+'\t.\t.\t') #Writes chromosome, position, id and reference base
                    f_vcf.write("DP="+components[3]) #Max depth?
                    f_vcf.write("\t") #Separates with tab to the next column
                    f_vcf.write("GT:AD:ADF:ADR\t0/1:"+components[3]+':'+str(count_forward)+':'+str(count_reverse)+'\n') #Total depth, forward depth and reverse depth
            #make_vcf_file.write_given_variant(vcf_file, components, count_forward, count_reverse, bases)

#Check that positions is indeed in bed regions, not outside them
def check_in_bedregion(values, components):
    for region in values.bed_regions[components[0]]: #balues.bed_regions is a dictionary, where keys are chromosomes, and values are lists with region tuples
        if region[0]<int(components[1])<=region[1]: #Region[0]=start in 0-base, components[1] real coordinate in 1-base, region[1] end region with 1-base
            return True
    return False #Position was not in area


#Goes stream line by line, counts how many lines have same number of reads covering sites and counts the total sum of genomic positions in the file
def stream_line_by_line(stream, values, report, vcf_file):
    undersized_count=0 #Initializes how many numbers are below the limit
    tot_average_sum=0 #Initializes total sum of reads more or less than given limit
    tot_average_count=0 #Initializes how many genomic positions have reads more or less than given limit
    limit=values.limit #Saves given limit
    lower=values.lower #Saves if user wants average of reads less or more than given limit
    lines_tot=0 #Count total number of genoic positions covered
    count = collections.Counter() #Make collection to store different numbers of reads and how many lines had certain amount of reads
    coverages=values.destination+'/'+patient_name.main(values.bam)+"_coverages"+datetime.now().strftime("%Y%m%dT%H%M%S")+".txt" #Create coverages file
    f_cov = open(coverages, "w+")
    f_cov.write("Here are genomic positions from file "+values.bam+". Made "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
    f_cov.write("Chr\tStart\tRef. base\tTotal depth\tForward depth\tReverse depth"+'\n')
    if vcf_file!=None:
        f_vcf= open(vcf_file, 'a') #Opens vcf file for appending
    else:
        f_vcf=None

    start_time2 = time.time()
    for line in stream.stdout: #Reads stdout line by line
        components = line.decode('utf-8').split() #Decodes line values and separate them
        if len(components) != 6 or int(components[3])==0: #If line isn't about reads or there are 0 reads covering site, it is skipped
            continue #Moves to next line
        if values.bed!='':
            if not check_in_bedregion(values, components):
                continue

        write_coverages_and_vcf_files(components, f_cov, f_vcf, values)

        lines_tot+=1 #Count line to total lines
        number = float(components[3]) #Fourth value contains number of reads covering site
        if number<limit: #If current number is smaller than given limit
            undersized_count+=1 #Amount of numbers below the limit increasees
        if lower and number<limit or not lower and number>limit: #If number is above or below (depending on the user) from given limit
            tot_average_sum+=number #Amount of reads covering site is added to total sum of numbers differing from the limit
            tot_average_count+=1 #Add position to differing positions
        count[number] += 1 #Count for that amount of reads covering site is added with one. Easy way to save numbers and their amount
    if lines_tot==0: #If there were no reads covering site and ignore=False (We are interested in the data)
        with open(report,'a') as f: #Open program report
            f.write("No reads covering sites were found.\n")
    else: #There were reads over 0 found, information is written to the report
        write_report_averages_and_limits(report, limit, undersized_count, lines_tot, tot_average_count, tot_average_sum, lower) #Writes to the report with function

    f_cov.close()
    if vcf_file!=None:
        f_vcf.close()
    return lines_tot, count #Returns total number of genomic positions and collection of numbers and their amounts.



#Makes the stream command and opens the stream
def stream_command(values):
    if values.include!=' ': #If there are flags that should be included
        include=' -f '+values.include+' ' #Makes included flags to right format for the stream
    else:
        include=' '
    if values.head!='': #If there is a head argument
        head = "|head -n "+values.head #Make head to right format for the stream
    else:
        head=''
    if values.bed!='': #If there is a given bed-file
        bed_command=' -L '+values.bed+' ' #Make bed command
    else:
        bed_command=''

    #if not reverse:
    stream = subprocess.Popen((samtools_location+' view '+values.other_args+' -b -F '+values.ignore+include+bed_command+values.bam+' | '+samtools_location+' mpileup \
      --ff 0 - -f '+values.reference+head), \
      shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #Open stream, first runs bedtools if given, then pipes it to samtools view. Finaly pipes everything to mpileup

    print(samtools_location+' view '+values.other_args+' -b -F '+values.ignore+include+bed_command+values.bam+' | '+samtools_location+' mpileup \
    --ff 0 - -f '+values.reference+head)

    return stream #Returns stream to further use


def plot_cdf_function(cdf_file, values):
    if values.bam_amount==1: #If there is only one file, plots different cumulative plot
        os.system('source '+r_env+' ; Rscript mutation_load_coverages_onefile.R '+cdf_file+datetime.now().strftime(" "+values.destination+"/cdf_%Y%m%dT%H%M%S.jpg")) #Gives 1 so R program now to plot 1 file plot
    else: #There are multiple files
        print('source '+r_env+' ; Rscript mutation_load_coverages_multiple_files.R '+cdf_file+datetime.now().strftime(" "+values.destination+"/cdf_%Y%m%dT%H%M%S.jpg ")\
        + datetime.now().strftime(values.destination+"/cdf_zoomed_%Y%m%dT%H%M%S.jpg"))
        os.system('source '+r_env+' ; Rscript mutation_load_coverages_multiple_files.R '+cdf_file+datetime.now().strftime(" "+values.destination+"/cdf_%Y%m%dT%H%M%S.jpg ")\
        + datetime.now().strftime(values.destination+"/cdf_zoomed_%Y%m%dT%H%M%S.jpg")) #Gives 2 to program so it nows what to plot


#Calls for stream_command-function, passes returned stream to stream_line_by_line function, counts genome size with whole_genome_length-function and returns numbers_tot and count
def counting_covered_positions(values, report, vcf_file, writer, fnames):

    stream=stream_command(values) #Get stream from stream_command
    numbers_tot, count  =  stream_line_by_line(stream, values, report, vcf_file) #Get total numbers and collection of different amount of reads covering sites from function.

    with open(report,'a') as f: #Opens program report for writing
        if values.bed=='': #Doesn't count whole genome length if bed was given
            genome_size=whole_genome_length(values.bam) #Get size of the whole reference genome with function
            f.write("The total length of the genome is "+str(genome_size)+" base pairs.\n") #Write how large the total genome is
        else:
            print("OK?")
            genome_size=bed_genome_length(values.bed)
            f.write("The total length of the BED file is "+str(genome_size)+" base pairs.\n") #Write how large the total genome is
        if genome_size>0:
            f.write(str(genome_size-numbers_tot)+" genomic positions ("+str(100*(genome_size-numbers_tot)/genome_size)+"%) were not covered with given filters.\n") #Write how many genomic positions were covered with file

    if values.number: #If user gave number that other reads covering site amounts should be compared to
        compare_one_number(values.bam, numbers_tot, count, values.more, values.number, report) #Compare other numbers to that one
    else: #User wants traditional CDF-function
        cdf_function(values.bam, numbers_tot, count, values.reverse, values.percent, report, writer, fnames, genome_size) #Writes CDF-function about different amount of reads covering sites

#Continues from permutation skipping CDF and creation of large VCF files
def continue_permutation(values):
    generated_vcf_files=list()
    all_vcf=dict()
    for root, dirs, files in os.walk(values.gen_vcf_location):
        for file in files:
            if not file.endswith(".vcf") or "permutated" in file or "temp_mutation" in file:
                continue
            else:
                all_vcf[root+file]=patient_name.main(root+'/'+file)
    #print(all_vcf)
    for file in values.bam: #Go through every given bam file
        found=False
        for vcf in all_vcf: #Go through every found VCF
            if all_vcf[vcf] in file: #If same sample id is found from bam and vcf, they are a match
                found=True
                generated_vcf_files.append(vcf)
                break
        if not found:
            print("Did not found VCF for file "+file+'\n')
    vcf_files=values.vcf_file.split()
    for vcf_file, generated_vcf_file in zip(vcf_files, generated_vcf_files):
        with open(values.report, 'a') as f_r:
            f_r.write(vcf_file+' '+generated_vcf_file+'\n')
        print(vcf_file, generated_vcf_file)
    permutate_vcf(values, generated_vcf_files, values.report)


#Makes bed command for samtools view
def make_bed_command(values):
    beds_splitted = values.bed.split() #Separates different bed files
    i=0 #Iterator for different bed files
    final_bed=values.destination+'/temp_bed_sorted_merged_expanded.bed'
    values.bed_regions=dict() #Memorizes all the bed regions, so later non-bed regions wont be counted
    for bed in beds_splitted: #For there is bed file
        os.system(bedtools_location+' sort -i '+bed+' > temp_bed_sorted.bed') #Sorts bed file
        os.system(bedtools_location+' merge -i temp_bed_sorted.bed > temp_bed_sorted_merged'+str(i)+'.bed') #Merges bed file
        os.remove(os.getcwd()+"/temp_bed_sorted.bed") #Removes temp sorted bed file
        i+=1 #Increases index
    if i>1: #If there were more than 1 bed file
        j=1 #another index
        string=bedtools_location+" intersect -a temp_bed_sorted_merged0.bed -b " #Initialize intersect command with first bed file
        while j<i: #While there is a bedfile
            string+='temp_bed_sorted_merged'+str(j)+'.bed ' #Add bed file to intersect command
            j+=1 #Increase index
        os.system(string+'> temp_bed_intersect.bed') #Store output to single bed file
        os.system(bedtools_location+"  merge -i temp_bed_intersect.bed > temp_bed_intersect_merged.bed") #Merge output bed file
        os.remove(os.getcwd()+"/temp_bed_intersect.bed") #Remove original intersect file
        j=0 #Initialize index
        while j<i: #Remove all single merged bed files
            os.remove(os.getcwd()+"/temp_bed_sorted_merged"+str(j)+".bed")
            j+=1
        os.rename(os.getcwd()+'/temp_bed_intersect_merged.bed',os.getcwd()+'/temp_bed_sorted_merged0.bed') #Rename intersect file to default file
    with open(os.getcwd()+'/temp_bed_sorted_merged0.bed', 'r') as fr:
        with open(final_bed, 'w+') as fw:
            for line in fr:
                columns=line.split()
                start=int(columns[1])
                end=int(columns[2])
                start+=values.flank_upstream
                end+=values.flank_downstream
                columns[1]=str(start)
                columns[2]=str(end)
                for column in columns:
                    fw.write(column+'\t')
                if not columns[0] in values.bed_regions:
                    values.bed_regions[columns[0]]=list()
                values.bed_regions[columns[0]].append((start,end))
                i+=1
                fw.write('\n')
    os.system("rm "+os.getcwd()+'/temp_bed_sorted_merged0.bed')
    values.bed=final_bed
    return values #Return values with bed file added
    #return ' -L temp_bed_sorted_merged0.bed ' #Return command


def start_from_beginning(values):
    report=make_report(values) #Function makes the program report
    if values.bed!='':
        values=make_bed_command(values)
    bam_files=values.bam #Add all bam files to bam_files variable so values.bam name can be changed on line 585
    generated_vcf_files=list() #Add all generated vcf files for vcf permutation
    if not values.number: #User wants CDF from all reads
        csv_file=values.destination+datetime.now().strftime("/cdf.%Y%m%dT%H%M%S.csv") #Make csv file for plotting
        csv_opened = open(csv_file, 'w+') #Open csv file for writing
        fnames=['bam_file', 'number_of_reads', 'amount_of_number', 'cumulative_sum', 'percent', 'interval'] #Make column names
        writer = csv.DictWriter(csv_opened, fieldnames=fnames) #Writer for csv writing
        writer.writeheader() #Write csv header
    for bam in bam_files: #Go through every file
        if not os.path.isfile(bam): #If bam does not exist
            raise NameError("Could not find bam file "+bam+' from directory '+os.getcwd()+'.\n') #Raises error
        with open(report, 'a') as f:
            f.write("\nCounted reads covering sites in bam file "+bam+'.\n')
        values.bam=bam #Save current bam file to values.bam
        if not values.no_vcf_generate:
            vcf_file=values.destination+'/'+patient_name.main(bam)+datetime.now().strftime("_%Y%m%dT%H%M%S.vcf") #Name for that vcf file of that bam file
            make_vcf_file.make_vcf(vcf_file,values.reference) #Makes vcf file
            generated_vcf_files.append(vcf_file) #Add coverages file's new vcf file to all vcf files
        else:
            vcf_file=None
        counting_covered_positions(values, report,vcf_file, writer, fnames) #Gets total amount of genomic positions in the file, makes CDF and returns coverages file
    if not values.number: #Went to for loop above: must close csv file and plot it
        csv_opened.close() #Closes csv file
        plot_cdf_function(csv_file, values) #Plots CDF function with R
    if not values.skip_perm: #If user has given vcf file
        permutate_vcf(values, generated_vcf_files, report) #Creates new vcf file with last coverage file
    #if values.bed!='':
#        os.system("rm "+values.bed)


def find_sample_ids(values):
    sample_ids=list()
    for file in values.bam:
        sample_id=patient_name.main(file)
        if sample_id in sample_ids:
            print("Sample id "+sample_id+" multiple times.")
        if sample_id==None:
            print("None: "+file)
    #    else:
    #        print(patient_name.main(file)+": "+file)
    exit()

def get_all_bam_files(directory): #Searches all bam files from the given directory and returns list of them
    if not os.path.isdir(directory): #Checks first that directory even exists
        optparser.error("Could not find directory "+directory+' from directory '+os.getcwd()+'.\n') #Directory was not found
    list_of_files=list() #Initializes list for bam files
    for root, dirs, files in os.walk(directory, topdown=True): #Goes through every directory, subdirectory and file in the starting_directory
        for file in files: #Every file in the directory
            if file.endswith('.bam'):
                list_of_files.append(root+'/'+file) #Adds file and its root to list
    return list_of_files #Returns all bam files


def check_optparsing(optparser,values):
    if values.bam==None and values.directory==None: #Checks that either file or directory is given
        optparser.error("Give file (-b /path/to/file) or directory (-d path/to/directory)") #Raises error if not
    if values.destination==None:
        optparser.error("Give destination directory for permutations, report etc.") #Raises error if not
    if not values.skip_perm and values.vcf_file==None:
        optparser.error("Give VCF-files corresponding to the BAM-files (--vcf_file \"path/to/file1.vcf path/to/file2.vcf\" or skip permutation by --skip_perm.")
    if not os.path.isdir(values.destination): #Checks that destination directory exists
        optparser.error("Could not find directory "+values.destination+' from directory '+os.getcwd()+'.\n') #Directory was not found
    if values.directory!=None: #If directory was given
        values.bam=get_all_bam_files(values.directory) #Searches all bam files from the directory
    else: #Directory was not given
        values.bam=values.bam.split() #Splits file argument in case there were multiple files given
    if values.cont_perm:
        if values.gen_vcf_location==None:
            optparser.error("Give directory containing generated VCF files (--gen_vcf_location path/to/directory)")
        if not os.path.isdir(values.gen_vcf_location):
            optparser.error("Could not find directory "+values.gen_vcf_location+' from directory '+os.getcwd()+'.\n') #Directory was not found
        if values.report==None:
            optparser.error("Give report file (--report path/to/file.txt)")
        if not os.path.isfile(values.report):
            optparser.error("Could not find file "+values.report+' from directory '+os.getcwd()+'.\n') #Directory was not found
        if values.skip_perm:
            optparser.error("Cant continue permutation (--continue) and skip it (--skip_permutation) at the same time.")
    if values.vcf_file!=None:
        if values.skip_perm:
            optparser.error("Do not give VCF files if you want to skip permutation.")
        for file in values.vcf_file.split():
            assert os.path.isfile(file), "Could not find file "+file+" from directory"+os.getcwd()+'.\n'
    assert not (not values.skip_perm and values.no_vcf_generate), "If you want to permutate VCF files, do not give parameter \"--no_vcf_generate\", since generated VCF files are needed for permutation. "
    "If you want to permutate VCF files, leave parameter \"--skip_perm\" out."
    if len(values.bam)>1: #There are multiple files
        values.bam_amount=2 #Argument so R program knows later how to plot the results
    else: #Only 1 file was given
        values.bam_amount=1 #Argument so R program knows later how to plot the results
    if not os.path.isdir(values.destination+'/'+"mutation_load_permutations"):
        os.mkdir(values.destination+'/'+"mutation_load_permutations")
    values.destination=values.destination+'/'+"mutation_load_permutations"
    return values


#Optparses user commands
def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog --bam example.bam --vcf_file example.vcf --destination example/dir [options]\n"
    "Counts CDF of read depths for a given bam file. If vcf file is given, permutates random mutations from bam file with the same occurence as in "
    "the given vcf file. Program creates directory for output to the given destination directory.") #Make header for help page
    #Add options to parser
    group = optparse.OptionGroup(optparser, "Input and output",
                    "Define your input files, output directory and if you want to keep annotations files.")
    group.add_option("-b", "--bam", dest="bam", help="Bam file(s) that will be read (-b /path/to/file)")
    group.add_option("-d", "--directory", dest="directory", help="If you want the program to run through all bam files in certain directory (-d /path/to/directory)")
    group.add_option("--vcf_file", dest="vcf_file", help="VCF file(s) for permutation (--vcf_file /path/to/file.vcf)")
    group.add_option("--destination", dest="destination", help="destination to cdf file, report etc. (--destination /path/to/directory)")
    group.add_option("--keep_anno", dest="keep_anno",action="store_true", default=False, help="If you want to keep generated anno files. Default: %default (Some files have same names, doesn't work perfectly)")
    group.add_option("--no_vcf_generate", dest="no_vcf_generate", action="store_true", default=False, help="If you do not want to generate VCF with all possible mutations. Needed in permutation. Default: %default.")
    group.add_option("--get_id_only", dest="get_id_only", action="store_true", default=False, help="If you want to check that program identifies the sample ids")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "Trimming and samtools options",
                    "With these options you can choose reference fasta file and exclude for example reads with certain bitflags or too little read depth.")
    group.add_option("--depth_lim", dest="depth_lim", default=10, type="int", help="Minimum depth to reads for coverages  and permutation files, default: %default")
    group.add_option("--rev_limit", dest="rev_limit", default=3, type="int", help="Minimum reverse depth for coverages and permutation files, default: %default")
    group.add_option("--for_limit", dest="for_limit", default=3, type="int", help="Minimum forward depth for coverages and permutation files, default: %default")
    group.add_option("--reference", dest="reference", default='/fs/vault/pipelines/gatk/data/homo_sapiens_v94/Homo_sapiens.GRCh38.dna.primary_assembly.fa', help="Reference fasta file (--reference /path/to/reference). Default: %default")
    group.add_option("-L", "--bed_file", dest="bed", default='', help="If you want to limit area to certain certain region with bedfile, write -L BEDFILE")
    group.add_option("--flank_upstream", dest="flank_upstream", default=0, type="int", help="How much you want to expand BED file coordinates to upstream. Default: %default")
    group.add_option("--flank_downstream", dest="flank_downstream", default=0, type="int", help="How much you want to expand BED file coordinates to downstream. Default: %default")
    group.add_option("-F", dest="ignore", default='0', help="Bit flags you want to ignore")
    group.add_option("-f", dest="include", default=' ', help="Bit flags you want to be set")
    group.add_option("--headn", dest="head", default='', help="If you want to limit area to certain size, write for example '-headn 10000'")
    group.add_option("--other", dest="other_args", default='', help="If you want to use other samtools view -arguments, write for example '-- other \"-q 10 -m 3\"'")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "CDF options",
                    "With these options you can decide information you want from CDF part")
    group.add_option("-p", "--percent", dest="percent", type="int", default=5, help="Percent with what distance the CDF-function will be at least printed, default: %default. For example '-p 5'.")
    group.add_option("-r", "--reverse", action="store_true", dest="reverse",  default=False, help="If you want to count CDF from largest to smallest, type -r. Default: %default")
    group.add_option("-n", "--number", dest="number", type="int", help="If you only want to know how many numbers have less reads than given number (or more when compared to -m).")
    group.add_option("-m", "--more", dest="more", default=False, action="store_true", help="If you want to know how many genomic positions have more reads than given number")
    group.add_option("-l", "--limit", dest="limit",type="int", default=1, help="Program writes how many genomic positions have more reads covering site than given limit. Default: %default")
    group.add_option("--lower", dest="lower",action="store_true", default=False, help="If you want to know average of reads below the limit, default is average of reads exceeding the limit")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "ANNOVAR options")
    group.add_option("--table_annovar", dest="table_annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/table_annovar.pl', help="Location of table_annovar.pl. Default: %default")
    group.add_option("--annovar", dest="annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/humandb_060418/', help="Location of annovar. Default: %default")
    group.add_option("--buildver", dest="buildver", default='hg38', help="Buildver version, default: %default")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "Permutation options",
                    "With these options you can for example decide which mutations you want to include and keep count on permutation")
    group.add_option("--skip_permutation", dest="skip_perm",action="store_true", default=False, help="If you do not want permutations")
    group.add_option("--separate_syn", dest="separate_syn",action="store_true", default=False, help="If you want same amount of syn. and nonsyn. as in input VCF. Ignoring non protein coding areas unless --intergenic has been given")
    group.add_option("--intergenic", dest="intergenic",action="store_true", default=False, help="If you want same amount of intergenic etc. as in input VCF")
    group.add_option("--perm_amount", dest="perm_amount", type="int", default=1, help="How many permutations you want for every bam, default: %default")
    group.add_option("--skip_nonexon", dest="skip_nonexon",action="store_true", default=False, help="If you want to skip all non exon mutations in permutation")
    optparser.add_option_group(group)

    group = optparse.OptionGroup(optparser, "Continue from permutation",
                    "If program crashed and you want to continue from the permutation, skipping the first part (CDF, generating VCFs containing all possible mutations...)."
                    " In addition, you need to specify bam files (-s path/to/file), original vcf files (--vcf_file ...), annovar, and permutation options.")
    group.add_option("--continue", dest="cont_perm", action="store_true", default=False, help="If you want to skip the first part")
    group.add_option("--gen_vcf_location", dest="gen_vcf_location", help="Directory containing generated large VCF files containing all possible mutations for every genomic position from bam files (recursive, subdirectories don't matter)")
    group.add_option("--report", dest="report", help="Original report from earlier run")
    optparser.add_option_group(group)

    (values, keys) = optparser.parse_args() #Separate values and keys from parser
    values=check_optparsing(optparser,values)
    return values #Returns optparser values


def main():
    print("JOTAIN OUTOA")
    values = optparsing() #Function makes the optparsing
    if values.get_id_only:
        find_sample_ids(values)
    if values.cont_perm:
        continue_permutation(values)
    else:
        start_from_beginning(values)


if __name__=='__main__': #If program is called directly
    start_time = time.time()
    main()
    print (time.time() - start_time, "seconds") #Prints consumed time
