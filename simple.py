# 


from optparse import OptionParser

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

    for line in content:
        print line.strip()


if __name__ == "__main__":
    main()

