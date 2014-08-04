import sys
import os
import ast
import collections

def convertFile(infile,outfile):
	f = open(infile)
	out = open(outfile,"w")

	lines = f.readlines()

	total_lines = len(lines)
	print "Total lines : ",total_lines
	count = 0
	for line in lines:
		point = ast.literal_eval(line.strip())
		out.write(str(flatten(point)) + "\n")
		
		count += 1
		if count % 10000 == 0:
			print "Done ",float(count*100.0)/total_lines,"%"

	f.close()
	out.close()


def flatten(d, parent_key=''):
    items = []
    for k, v in d.items():
        new_key = parent_key + '/' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)

if __name__ == "__main__":
	convertFile(sys.argv[1],sys.argv[2])
