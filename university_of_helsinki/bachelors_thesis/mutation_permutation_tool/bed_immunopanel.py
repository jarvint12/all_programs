import optparse
import os


# Takes gene containing list of important genes as well as flanking parameters. Creates new bed file containing only those genes, with specified flanking.

#python3 bed_immunopanel.py --important_genes_file immunopanel.txt --flank_upstream 5 --flank_downstream 5
def create_new_bed(values):
    important_genes=list()

    new_bed_name="/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/immunopanel_genes.bed"
    new_bed=open(new_bed_name, 'w+')
    without_flanks=open("/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/immunopanel_genes_without_flanks.bed", 'w+')
    with open(values.important_genes_file, mode='r', encoding='utf-8-sig') as fr:
        for line in fr.readlines():
            columns=line.split()
            important_genes.append(columns[0].strip())
    #print(important_genes)
    found_genes=list()
    with open(values.refgene_file, 'r') as fr:
        for line in fr.readlines():
            columns=line.split() #0: bin, 1: name, 2: chrom, 3: strand (+/-), 4: TranscriptionStart, 5: txEnd, 6: Coding region Start, 7: cdsEnd, 8: Number of exons, 9:exonStarts, 10: exonEnds (separated by commas), 11:score, 12: name2, 13: cdsStartStat, 14: cdsEndStat, 15: exonFrames
            name=columns[12].strip()
            if not name in important_genes:
                continue
            found_genes.append(name)
            strand=columns[3].strip()
            starts=columns[9].strip().split(',')
            ends=columns[10].strip().split(',')
            score=columns[11].strip()
            chrom=columns[2].strip()
            for start, end in zip(starts, ends):
                if start=='':
                    continue
                without_flanks.write(chrom+'\t'+start+'\t'+end+'\t'+name+'\t'+score+'\t'+strand+'\n')
                if strand=="-": #Upstream is the second, R
                    new_bed.write(chrom+'\t'+str(int(start)-values.flank_downstream)+'\t'+str(int(end)+values.flank_upstream)+'\t'+name+'\t'+score+'\t'+strand+'\n')
                elif strand=="+": #Upstream is the first, L
                    new_bed.write(chrom+'\t'+str(int(start)-values.flank_upstream)+'\t'+str(int(end)+values.flank_downstream)+'\t'+name+'\t'+score+'\t'+strand+'\n')
                else: #Strand is 'unk'
                    new_bed.write(chrom+'\t'+str(int(start)-values.flank_downstream)+'\t'+str(int(end)+values.flank_upstream)+'\t'+name+'\t'+score+'\t'+strand+'\n')
    new_bed.close()
    without_flanks.close()
    for gene in important_genes:
        if not gene in found_genes:
            print("Gene not found: "+gene)
    os.system("sed -i \"s/chr//g\" "+new_bed_name)

def check_optparsing(optparser, values):
    assert values.important_genes_file!=None, "Give file containing important genes"
    assert os.path.isfile(values.important_genes_file), "Could not find file "+values.important_genes_file+" from directory "+os.getcwd()
    assert os.path.isfile(values.refgene_file), "Could not find file "+values.refgene_file+" from directory "+os.getcwd()    -

def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [options]\n\
    Creates new bedfile with flanking to upstream and downstream.") #Make header for help page
    optparser.add_option("--important_genes_file", dest="important_genes_file", help="File containing important genes")
    optparser.add_option("--refgene_file", dest="refgene_file", default="/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/humandb_060418/hg38_refGene.txt", help="ANNOVAR refGene file, default: %default")
    optparser.add_option("--flank_upstream", dest="flank_upstream", default=0, type="int", help="How much you want to expand BED file coordinates to upstream. Default: %default")
    optparser.add_option("--flank_downstream", dest="flank_downstream", default=0, type="int", help="How much you want to expand BED file coordinates to downstream. Default: %default")
    (values, keys) = optparser.parse_args()
    check_optparsing(optparser, values)
    return values

def main():
    values=optparsing()
    create_new_bed(values)

if __name__=='__main__':
    main()
