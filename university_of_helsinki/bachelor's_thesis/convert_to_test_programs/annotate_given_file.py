import os
import subprocess
import optparse



def get_line_count(file, is_vcf):
    if is_vcf:
        p = subprocess.Popen('cat '+file+' | grep -v "#" | wc -l', shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
        out, err = p.communicate()
        return int(out.decode().strip())+1 #header
    else:
        p = subprocess.Popen('cat '+file+' | wc -l', shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
        out, err = p.communicate()
        return int(out.decode().strip())



def annotate_file(values):
    print('time '+values.table_annovar+' '+values.vcf_path+' '
    +values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+
    values.destination+'/'+values.sample_id+'/'+values.sample_id_number)
    size=0
    line_count=0
    vcf_line_count=get_line_count(values.vcf_path, True)
    while not os.path.isfile(values.destination+'/'+values.sample_id+'/'+values.sample_id_number+'.hg38_multianno.txt') or size==0 or line_count==1 or line_count!=vcf_line_count:
        os.system("rm "+values.destination+'/'+values.sample_id+'/'+values.sample_id_number+'*')
        os.system('time '+values.table_annovar+' '+values.vcf_path+' '
        +values.annovar+' -buildver '+values.buildver+' -otherinfo -remove --vcfinput -protocol refGene,dbnsfp33a -operation g,f -out '+
        values.destination+'/'+values.sample_id+'/'+values.sample_id_number)
        if os.path.isfile(values.destination+'/'+values.sample_id+'/'+values.sample_id_number+'.hg38_multianno.txt'):
            line_count=get_line_count(values.destination+'/'+values.sample_id+'/'+values.sample_id_number+'.hg38_multianno.txt', False)
            size=os.path.getsize(values.destination+'/'+values.sample_id+'/'+values.sample_id_number+'.hg38_multianno.txt')



def optparsing():
    optparser = optparse.OptionParser(usage= "python3 %prog [options]\n\
    Gets directory as parameter and annotates every file in it") #Make header for help page
    optparser.add_option("--sample_id", dest="sample_id", help="Sample id of file")
    optparser.add_option("--sample_id_number", dest="sample_id_number", help="Sample id with number")
    optparser.add_option("--vcf_path", dest="vcf_path", help="Path to VCF file")
    optparser.add_option("--destination", dest="destination",
    default="/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool//reports_permutation_HRUH/all_permutations/aa_samples/annotations2/", help="Destination for annotation files")

    group = optparse.OptionGroup(optparser, "ANNOVAR options")
    group.add_option("--table_annovar", dest="table_annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/table_annovar.pl', help="Location of table_annovar.pl. Default: %default")
    group.add_option("--annovar", dest="annovar", default='/fs/vault/pipelines/rnaseq/bin/2.7.0/annovar/humandb_060418/', help="Location of annovar. Default: %default")
    group.add_option("--buildver", dest="buildver", default='hg38', help="Buildver version, default: %default")
    optparser.add_option_group(group)

    (values, keys) = optparser.parse_args()
    return values

def main():
    values=optparsing()
    annotate_file(values)




if __name__=='__main__':
    main()
