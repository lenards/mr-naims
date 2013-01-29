

fname = 'test-set.txt'

with open(fname) as f:
    content = f.readlines()

for line in content:
    print line.strip()


