#######################################################
# NeXML reading/writing for Simple name Cleaner
#   produced at Phylotastic-II / NESCent::HIP
# 
# TNRS Team: Dan Leehr, Andrew Lenards, Guarav Vaidya
#######################################################

# Not yet called by the cleaner
import dendropy

class Naixml:
    def __init__(self,filename):
        self.tree = dendropy.Tree.get_from_path(filename, 'nexml')

    def write_tree(self,outputname):
        with open(outputname,'w') as out:
            self.tree.write(out,'nexml')
    
    def get_otu_labels(self):
        return [t.label for t in self.tree.taxon_set]

    def get_node_labels(self):
        return [n.label for n in self.tree.get_node_set()]

    def replace_otu_labels(self,mapping):
        # dict of old: new
        # Ideally would include the URIs and fancy things, but this is first stab
        for key in mapping:
            print "OTU: changing %s to %s" % (key, mapping[key])
            self.tree.taxon_set.get_taxon(label=key).label=mapping[key]

    def replace_node_labels(self, mapping):
        for key in mapping:
            print "Node: changing %s to %s" % (key, mapping[key])
            self.tree.find_node_with_label(key).label=mapping[key]

# For simple testing, read in a nexml file, 
# change a label, and write out a new file
naix = Naixml('sampletree-nexml.xml')
mapping = {'Tsukamurella paurometabola': 'CHANGED Tsukamurella paurometabola CHANGED'}
naix.replace_otu_labels(mapping)
naix.replace_node_labels(mapping)
# now write out the new tree
naix.write_tree('sampletree-nexml-changed.xml')
