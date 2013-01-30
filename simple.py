# 
import requests
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
    
def main():
    (options, args) = get_args()

    fname = grab_file(options, args)

    with open(fname) as f:
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

    with open(fname + '.clean', 'w') as out:
        for key in mapping.keys():
            val = mapping[key]
            print val
            if (val != None):
                out.write(val + '\n')
            else:
                out.write(key + '\n')

#    print mapping

if __name__ == "__main__":
    main()

