# 
import requests
import codecs
import time
from optparse import OptionParser

taxosaurus_base="http://taxosaurus.org/"
MATCH_THRESHOLD=0.9

def lookup_taxosaurus(name):
    payload={'query': name}
    response = requests.post(taxosaurus_base + 'submit',params=payload)
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

# Returns the assumed input file
def grab_file(options, args):
    """
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

# Returns the mapping of input to clean names and a report of all
# actions taken
def create_name_mapping(names):

    # A match JSON object from
    #
    # {
    #     u'sourceId': u'iPlant_TNRS',
    #     u'acceptedName': u'Spartina',
    #     u'uri': u'http: //www.tropicos.org/Name/40002506',
    #     u'matchedName': u'Spartina',
    #     u'score': u'0.4945992525683',
    #     u'annotations': {
    #         u'Authority': u'Schreb.'
    #     }
    # }

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
                if (accepted != ""):
                    mapping[submittedName] = accepted

    return mapping, prov_report


def main():
    global MATCH_THRESHOLD
    (options, args) = get_args()

    fname = grab_file(options, args)
    if (options.m_threshold != None and options.m_threshold != MATCH_THRESHOLD):
        MATCH_THRESHOLD = float(options.m_threshold)

    with codecs.open(fname, 'r', encoding='utf-8') as f:
        content = f.readlines()
        result = lookup_taxosaurus(''.join(content))
#        print result

    (mapping, prov_report) = create_name_mapping(result['names'])

    replace_names(mapping, fname, fname + '.clean')

if __name__ == "__main__":
    main()

