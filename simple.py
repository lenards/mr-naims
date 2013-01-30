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
        print result


if __name__ == "__main__":
    main()

