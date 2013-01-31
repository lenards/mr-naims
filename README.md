mr-naims
========

A simple name cleaner in python using the [Phylotastic TNRastic API](http://www.evoio.org/wiki/Phylotastic/TNRS) at [Taxosaurus](http://taxosaurus.org)

### Dependencies

* Python 2.7.  You should run mr-naims in a [virtualenv](http://www.virtualenv.org/)
* [Requests: HTTP for humans](http://docs.python-requests.org/en/latest/).  Install it in your virtualenv with `pip install requests`

### Usage

     simple.py [options] --file file-input
     
Where file-input is a list of species names to be cleaned in text format, one per line, or a PDF file.  The `test-set.txt` is included as an example.  If a PDF file is provided, mr-naims uses [Global Names Recognition and Discovery](http://gnrd.globalnames.org) to extract scientific names from the PDF text.

mr-naims producecs a `<filename>.clean` file with the cleaned list, as well as a CSV report including the match score and provenance of each result.
