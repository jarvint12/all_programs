import re
import sys

def sample_id_filename(file):

    sample_id=None #Keep count if sample_id is found

    pattern_patient=re.compile(r'\d{6}_.{6}_\d{4}_.{10}_.*_\w\d{3}_\w\d{3}') #Tries to find Epi-Ski-type sample_id
    matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    for match in matches_sampleid: #Check if sample_id type 'Epi-Ski'
        sample_id = match.group(0)[30:len(match.group(0))-10] #Sample_id separated
    # if sample_id==None: #If sample_id was not Epi-Ski, search for sample_if more widely
    #     pattern_patient2 = re.compile(r'/(S\d+(_\d+)?|SRR\d+|[A-Z]+_\d+|\d+_[A-Z]+)[._]') #Check for sample_id in the filename more widely
    #     matches_sampleid2 = pattern_patient2.finditer(file)
    #     for match in matches_sampleid2:
    #         sample_id = match.group(0)[1:len(match.group(0))-1] #Separates the sample_id from match
    return sample_id

def is_vcf_file(file):
    pattern_vcf = re.compile(r'.*\.(vcf(\.idx)?|bcf)$') #Vcf-files endings in pattern
    matches_vcf = pattern_vcf.finditer(file) #Checks for vcf-file-ending from a filename
    for match in matches_vcf: #Checks if file had vcf-ending
        return True #If it had, file is a vcf-file
    return False #File was not a vcf file

def sample_id_vcf_file(file):
    pattern = re.compile(r'TUMOR,SampleName=[A-Z]+_?\d+') #First, let's try to find sample name from file with the most reliable way from file
    matches = pattern.finditer(file) #Searches for pattern in file
    sample_id=None
    for match in matches: #Checks if there are any matches
        i=i+1 #If match was found, increases i. If many matches are found i>1
        if i>1: #If multiple matches are found, they are compared
            if match.group(0)[17:]!=sample_id: #Compares new match to the previous
                return None #Returns that sample_id=None if two matches differentiate, because then sample_id can't be recognized
        sample_id = match.group(0)[17:] #Separates sample_id from new match

    if sample_id==None: #If sample_id still wasn't found from file
        pattern2 = re.compile(r'gatk/(S\d+(_\d+)?|SRR\d+|[A-Z]+_\d+|\d+_[A-Z]+)[_.]') #Second, program tries to find sample name from file with gatk/
        matches=pattern2.finditer(file) #Searches for pattern in file
        for match in matches: #Checks if there are matches
            i=i+1 #If match was found, increases i. If many matches are found i>1
            if i>1: #If multiple matches are found, they are compared
                if match.group(0)[17:]!=sample_id: #Compares new match to the previous
                    return None #Returns that sample_id=None if two matches differentiate, because then sample_id can't be recognized
            sample_id = match.group(0)[5:len(match.group(0))-1] #Separates sample_id from rest of the pattern

    return sample_id

def sample_id_vcf_epi(file):
    sample_id=None
    pattern_patient=re.compile(r'/[Ee][^/]*\d_') #Tries to find Epi-Ski-type sample_id
    matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    for match in matches_sampleid:
        sample_id=match.group(0)[1:-1]
    return sample_id

def sample_id_aa(file):
    sample_id=None
    pattern_patient=re.compile(r'/[^/]*_(\w\w_\w\w\d|\d\d?_(\w|\d)\d)_') #Tries to find Epi-Ski-type sample_id
    matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    for match in matches_sampleid:
        sample_id=match.group(0)[1:-1]
    pattern_patient=re.compile(r'(HRUH|FH)[^/]*_(\w\w_\w\w\d_|\d\d?_(\w|\d)\d_|CD(4|8)_)(\w\w\w\d\d_|\d\d-\d\d_)?([a-z]{3}\d{2}_)?') #Tries to find Epi-Ski-type sample_id HRUH581_PB_CD4 FH_6288_2_D1 FHRB_892_2_D1 FHRB3801_BM_CD4_jul14 FHRB3696_MNC_3_14 FHRB613_PB_CD8 FHRB1182_CD4
    matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    for match in matches_sampleid:
        sample_id=match.group(0)[:-1]
    return sample_id
    # if '_CD' in file:
    #      pattern_patient=re.compile(r'/\d{6}_.{6}_\d{4}_.{10}_.*_(\w\w_)?CD\d_')
    # else:
    #     pattern_patient=re.compile(r'/\d{6}_.{6}_\d{4}_.{10}_.*_\d\d?_(\w|\d)\d_') #Tries to find Epi-Ski-type sample_id
    # matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    # for match in matches_sampleid: #Check if sample_id type 'Epi-Ski'
    #     return match.group(0)[31:-1]
    # if '_CD' in file:
    #     pattern_patient=re.compile(r'/\d{6}_.{5}_\d{4}_.{10}_.*_(\w\w_)?CD\d_') #Tries to find Epi-Ski-type sample_id
    # else:
    #     pattern_patient=re.compile(r'/\d{6}_.{5}_\d{4}_.{10}_.*_\d\d?_(\w|\d)\d_') #Tries to find Epi-Ski-type sample_id
    # matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    # for match in matches_sampleid: #Check if sample_id type 'Epi-Ski'
    #     return match.group(0)[30:-1]
    # pattern_patient=re.compile(r'HRUH\d+_\w\w_\w\w\d') #Tries to find Epi-Ski-type sample_id
    # matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    # for match in matches_sampleid: #Check if sample_id type 'Epi-Ski'
    #     return match.group(0)
    return None

def sample_id_vcf_aa(file):
    sample_id=None
    pattern_patient=re.compile(r'/[^/]*_(\w\w_\w\w\d|\d\d?_(\w|\d)\d)_') #Tries to find Epi-Ski-type sample_id
    matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    for match in matches_sampleid:
        sample_id=match.group(0)[1:-1]
    pattern_patient=re.compile(r'(HRUH|FH)[^/]*_(\w\w_\w\w\d_|\d\d?_(\w|\d)\d_|CD(4|8)_)(\w\w\w\d\d_|\d\d-\d\d_)?([a-z]{3}\d{2}_)?') #Tries to find Epi-Ski-type sample_id HRUH581_PB_CD4 FH_6288_2_D1 FHRB_892_2_D1 FHRB3801_BM_CD4_jul14 FHRB3696_MNC_3_14 FHRB613_PB_CD8 FHRB1182_CD4
    matches_sampleid = pattern_patient.finditer(file) #Check, if there is sample_id in the filename
    for match in matches_sampleid:
        sample_id=match.group(0)[:-1]
    return sample_id


def number_id(file):
    sample_id=None
    pattern_patient=re.compile(r'\d*_CD\d_')
    matches_sampleid=pattern_patient.finditer(file)
    for match in matches_sampleid:
        sample_id=match.group(0)[:-1]
    return sample_id

def shady(file):
    sample_id=None
    pattern_patient=re.compile(r'/(FM_|FM)?\d\d\d\d?(_S\d\d?|[-_]?[A-Z]*\d?)?') #FM_761, FM1641_S13, FM630_S7 | 711_D, 637-D,892_G8
    matches_sampleid=pattern_patient.finditer(file)
    for match in matches_sampleid:
        sample_id=match.group(0)[1:]
    return sample_id

def main(file):
    sample_id=sample_id_filename(file) #Tries to find sample_id from file name
    #if sample_id==None: #Sample_id was not in the file name
    #    if is_vcf_file(file): #Checks if file is a vcf file
    #        sample_id = sample_id_vcf_file(file) #Tries to find file name inside vcf file
    if sample_id==None: #If sample_id was still not found
        sample_id=sample_id_vcf_epi(file)
    if sample_id==None:
        sample_id=sample_id_aa(file)
    if sample_id==None: #If sample_id was still not found
        sample_id=sample_id_vcf_aa(file)
    if sample_id==None:
        sample_id=number_id(file)
    if sample_id==None:
        sample_id=shady(file)
    #if sample_id==None:
    #    print("\n"+file+": TUNTEMATOn\n")
    return sample_id #Returns sample_id


if __name__ == '__main__':
    print(main(sys.argv[1]))
