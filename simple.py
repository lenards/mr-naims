#######################################################
# Simple Name Cleaner 
#   produced at Phylotastic-II / NESCent::HIP
# 
# TNRS Team: Dan Leehr, Andrew Lenards, Guarav Vaidya
#######################################################
import requests
import codecs
import csv
import time
import json
from optparse import OptionParser

taxosaurus_url="http://taxosaurus.org/"
gnrd_url='http://gnrd.globalnames.org/name_finder.json'
MATCH_THRESHOLD=0.9

def lookup_taxosaurus(names):
    print "calling taxosaurus"
    payload={'query': '\n'.join(names)}
    response = requests.post(taxosaurus_url + 'submit',params=payload)
    while response.status_code == 302:
        time.sleep(0.5)
        response = requests.get(response.url)
    return response.json()


def get_args():
    m_thres_help = ("the matching score threshold to use, defined as a " \
                   "decimal, all matches equal to or greater will be replaced." \
                   " The default is %s") % MATCH_THRESHOLD
    usage = "usage:\n %prog [options] file-input\n or\n %prog [options] --file file-input"

    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--file", dest="filename",
              help="the file, FILE, read from...", metavar="FILE")
    parser.add_option("--match-threshold", dest="m_threshold", 
              default=MATCH_THRESHOLD, help=m_thres_help, 
              metavar="MATCH_SCORE_THRESHOLD")
    return parser.parse_args()


def grab_file(options, args):
    """
    Returns the assumed input file

    If the --file/-f argument is not pass in, assume the first
    positional argument is the filename to operate on
    """
    if (options.filename == None):
        return args[0]
    return options.filename

def replace_names(mapping, source_filename, dest_filename):
    with codecs.open(source_filename, 'r', encoding='utf-8') as source:
        with codecs.open(dest_filename, 'w', encoding='utf-8') as dest:
            for line in source:
                key = line.rstrip()
                if key in mapping.keys():
                    val = mapping[key]
                    if (val != None):
                        line = val + '\n'
                dest.write(line)


def replace_names(names, mapping):
    """
    names is the original list
    mapping is the dictionary
    """
    results = []
    for name in names:
        if name in mapping.keys():
            results.append(mapping[name])
        else:
            results.append(name)
    return results


def get_best_match(matches, minscore):
    """
    Returns the best match from the list of matches,
    provided that the minimum score is exceeded
    """ 
    # Filter to the matches that meet the minimum score
    filtered = [m for m in matches if float(m['score']) >= minscore]
    if (len(filtered) == 0):
        # Nothing in the list met the minimum score
        return None 
    else:
        # sort by score and return the highest
        return sorted(filtered, key=lambda k: float(k['score']))[-1]


def log_record_in(report, name, match, matches):
    """
    Mutate the report's record for a given submitted name
    """
    prov_record = report[name]
    prov_record['submittedName'] = name
#   prov_record['otherMatches'] = json.dumps(matches)
    if not match:
        prov_record['accepted'] = 'none'
    # if there's no match, then skip this
    else:
        prov_record['accepted'] = match['acceptedName']
        prov_record['sourceId'] = match['sourceId']
        prov_record['uri'] = match['uri']
        prov_record['score'] = match['score']


def create_name_mapping(names):
    """
    Returns the mapping of input to clean names and a report of all
    action taken
    """
    mapping = dict()
    prov_report = dict() 

    for name in names:
        matches = name['matches']
        submittedName = name['submittedName']

        prov_report[submittedName] = dict()

        if (len(matches) >= 1):
            match = get_best_match(matches, MATCH_THRESHOLD)
            if match:
                # match met the minimum, create a mapping
                accepted = match['acceptedName']
                log_record_in(prov_report, submittedName, match, matches)

                if (accepted != ""):
                    mapping[submittedName] = accepted
            else:
                log_record_in(prov_report, submittedName, match, matches)

    return mapping, prov_report


def get_names_from_file(filename):
    """
    Returns a list of names.
    If the file is a text file, it is assumed that there is one name per line
    If the file is a PDF file, it is sent to http://gnrd.globalnames.org/api
    for name recognition, and the resultant list is returned
    """
    names = []
    if(filename.lower().endswith('.pdf')):
        # PDF file
        # needs to be multipart/form-data
        files={'file': ('filename.pdf', open(filename,'rb'))}
        params={'unique':'true'}
        print "calling gnrd"
        response = requests.get(gnrd_url, params=params, files=files)
        print response.status_code
        while response.json()['status'] == 303:
            print response.text
            time.sleep(0.5)
            response = requests.get(response.url)
        names = [x['scientificName'] for x in response.json()['names']]
    else:
        # text file
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                names.append(line.rstrip())
    return names

#######################################################
# just testing the prov_report written to standard out
import sys
#######################################################

def main():
    global MATCH_THRESHOLD
    (options, args) = get_args()

    fname = grab_file(options, args)
    if (options.m_threshold != None and options.m_threshold != MATCH_THRESHOLD):
        MATCH_THRESHOLD = float(options.m_threshold)

    names = get_names_from_file(fname)
    result = lookup_taxosaurus(names)
    (mapping, prov_report) = create_name_mapping(result['names'])

#    fields = ('submittedName','accepted','sourceId','uri','score','otherMatches')
    fields = ('submittedName','accepted','sourceId','uri','score')

    headers = dict((field,field) for field in fields)

    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writerow(headers)
    for record in prov_report.keys():
        writer.writerow(prov_report[record])

    replaced = replace_names(names, mapping)
    # For now, just write the list out to file
    with codecs.open(fname + '.clean', 'w', encoding='utf-8') as dest:
        for item in replaced:
            dest.write(item + '\n')



if __name__ == "__main__":
    main()

