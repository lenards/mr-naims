# 
import requests
import codecs
from optparse import OptionParser

taxosaurus_base="http://taxosaurus.org/"

def lookup_taxosaurus(name):
    payload={'query': name}
    response = requests.post(taxosaurus_base + 'submit',params=payload)
    while response.status_code == 302:
        response = requests.get(response.url)
    return response.json()

def get_args():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
              help="the file, FILE, read from...", metavar="FILE")

    return parser.parse_args()

def grab_file(options, args):
    if (options.filename == None):
        return args[0]
    return options.filename

def replace_names(mapping, source_name, dest_name):
    with codecs.open(source_name, 'r', encoding='utf-8') as source:
        with codecs.open(dest_name, 'w', encoding='utf-8') as dest:
            for line in source:
                for key in mapping.keys():
                    val = mapping[key]
                    if (val != None):
                        line = line.replace(key,val)
                dest.write(line)
    
def main():
    (options, args) = get_args()

    fname = grab_file(options, args)

    with codecs.open(fname, 'r', encoding='utf-8') as f:
        content = f.readlines()
        result = lookup_taxosaurus(''.join(content))
#        print result

    names = result['names']
    mapping = dict()

    for name in names:
        matches = name['matches']
        submittedName = name['submittedName']
        if (len(matches) >= 1):
            # grab the first match for now
            match = matches[0]
            accepted = match['acceptedName'] 
            if (accepted != ""):
                mapping[submittedName] = accepted

    replace_names(mapping, fname, fname + '.clean')

if __name__ == "__main__":
    main()

