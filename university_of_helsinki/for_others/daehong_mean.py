import subprocess


def count_IQR(dps,avg):

    n=len(dps)
    i=n//2
    half_samples=n//2+(n%2>0)
    if n%2>0: #n is odd
        if abs(avg-dps[i])>=abs(avg-dps[i+1]): #Choose the one closer to the mean
            i+=1
    j=0
    min_side=avg-dps[i]
    max_side=avg-dps[i]
    move_left=1
    move_right=1
    while j<half_samples:
        #print("LEFT: ","DPS[i]",dps[i],"-","DPS[move_left]",dps[i-move_left],"=",abs(dps[i]-dps[i-move_left]))
        #print("Right: ","DPS[i]",dps[i],"-","DPS[move_right]",dps[i+move_right],"=",abs(dps[i]-dps[i-move_right]))
        #print(abs(dps[i]-dps[i-move_left])<abs(dps[i]-dps[i+move_right]))
        if abs(dps[i]-dps[i-move_left])<abs(dps[i]-dps[i+move_right]): #left is closer to average, includes it
            min_side=dps[i-move_left]
        #    print("NEW MIN",min_side)
            move_left+=1
        else:
            max_side=dps[i+move_right]
        #    print("NEW MAX",max_side)
            move_right+=1
        j+=1
    print(dps)

    return min_side, max_side




def averages(whole_length):
    with open("/mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin yliopisto/daehong/cdf.20210219T174612.csv", 'r') as fr:
    #with open("/csc/mustjoki2/variant_move/epi_ski/daehong/mutation_load_permutations/cdf.20210127T184239.csv", 'r') as fr:
        total_seq=0
        total_positions=0
        total_seq_single=0
        total_positions_single=0
        pos_dps=list()
        gen_dps=list()

        max_single_avg_cov_pos=float('-inf')
        min_single_avg_cov_pos=float('inf')
        max_single_avg_cov_genome=float('-inf')
        min_single_avg_cov_genome=float('inf')
        last_sample_id=None
        for line in fr.readlines()[1:]:
            columns=line.split(',')
            if columns[0]!=last_sample_id and last_sample_id!=None:
                print(last_sample_id, columns[0])
                single_avg_cov_pos=total_seq_single/total_positions_single
                pos_dps.append(single_avg_cov_pos)
                single_avg_cov_genome=total_seq_single/whole_length
                gen_dps.append(single_avg_cov_genome)
                last_sample_id==columns[0]
                total_positions_single=0
                total_seq_single=0
                last_sample_id=columns[0]
            if last_sample_id==None:
                last_sample_id=columns[0]
            total_seq+=int(columns[1])*int(columns[2])
            total_positions+=int(columns[2])
            total_positions_single+=int(columns[2])
            total_seq_single+=int(columns[1])*int(columns[2])
        pos_dps.sort()
        gen_dps.sort()
        print(gen_dps)
        print("Average DP on all covered genomic positions: "+str(total_seq/total_positions))
        print("Average DP on whole genome: "+str(total_seq/(28*whole_length)))
        print("Whole genome length: "+str(whole_length))
        print("Single whole genome avg DP min: "+str(min(gen_dps))+" max: "+str(max(gen_dps)))
        print("Single covered positions avg DP min: "+str(min(pos_dps))+" max: "+str(max(pos_dps)))
        avg_pos=total_seq/total_positions
        avg_gen=total_seq/(28*whole_length)
        print("Counting IQR")
        min_iqr_pos, max_iqr_pos= count_IQR(pos_dps, avg_pos)
        print("AVG",avg_pos)
        print("Position average IQR: "+str(min_iqr_pos)+"-"+str(max_iqr_pos))
        print("Compared to average: "+str(min_iqr_pos-avg_pos)+", "+str(max_iqr_pos-avg_pos))
        min_iqr_gen, max_iqr_gen=count_IQR(gen_dps, avg_gen)
        print("AVG",avg_gen)
        print("Genome average IQR: "+str(min_iqr_gen)+"-"+str(max_iqr_gen))
        print("Compared to average: "+str(min_iqr_gen-avg_gen)+", "+str(max_iqr_gen-avg_gen))

def over_ten_shady():
    file="/mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin yliopisto/shady/cdf.20210204T183248.csv"
    previous=None
    with open(file, 'r') as fr:
        for line in fr.readlines()[1:]:
            columns=line.split(',')
            if previous!=columns[0]:
                if previous==None:
                    print("Sample\tBP with DP>=10\tTot coverage of BP>=10\tAvg coverage of BP with DP>=10")
                else:
                    print(previous+"\t"+str(tot_bp)+'\t'+str(tot_cov)+'\t'+str(round(tot_cov/tot_bp)))
                previous=columns[0]
                tot_bp=0
                tot_cov=0
            depth=int(columns[1])
            if depth<10:
                continue
            amount_of_bps=int(columns[2])
            tot_bp+=amount_of_bps
            tot_cov+=depth*amount_of_bps

def whole_genome_length(file):
    stream = subprocess.Popen(('/fs/vault/pipelines/microbiology/bin/1.0.0/samtools-1.7/samtools view -h '+file), \
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


def main():
    bed=True
    if not bed:
        file="/csc/mustjoki/gatk/aa_genotype/gatk//160330_D00482_0111_AC8LG3ANXX_FHRB1641_BM_CD4_10-15_CTGAAGCT-GGCTCTGA_L004.trimmed.merge.final.bam"
        whole_length=whole_genome_length(file)
    else:
        bed_file="/mnt/c/Users/TimoJ/Documents/Työpaikat/Helsingin yliopisto/daehong/temp_bed_sorted_merged_expanded.bed"
        whole_length=bed_genome_length(bed_file)
    averages(whole_length)
    #over_ten_shady()


if __name__=='__main__':
    main()
