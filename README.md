mr-naims
========

A simple name cleaner in python using the [Phylotastic TNRastic API](http://www.evoio.org/wiki/Phylotastic/TNRS) at [Taxosaurus](http://taxosaurus.org).  

mr-naims is a [Phylotastic 2](http://evoio.org/wiki/Phylotastic) project 

### Dependencies

* Python 2.7.  You should run mr-naims in a [virtualenv](http://www.virtualenv.org/)
* [Requests: HTTP for humans](http://docs.python-requests.org/en/latest/).  Install it in your virtualenv with `pip install requests`
* [DendroPy](http://packages.python.org/DendroPy/), for reading Newick and NeXML trees.  `pip install dendropy`.

### Usage

     python simple.py [options] -f inputfile
     
inputfile may be a PDF, image, Office Document, Text file, Newick tree, or [NeXML file](http://www.nexml.org) (NeXML support is experimental).  It will be sent to [Global Names Recognition and Discovery](http://gnrd.globalnames.org) to extract a list of scientific names, unless you specify -s/--skip-gnrd.  Run `python simple.py -h` for help.
If providing a newick tree, specify the -n option.

If you would like to limit the TNRS search to a specific provider, use the --source option, e.g. `--source MSW3`

The `test-set.txt` is included as an example list of names

mr-naims producecs a `inputfile.clean` file containing the cleaned list, and outputs a CSV report including the match score and provenance of each result.

### Known Issues

There are issues at the TNRS level with unicode names.
