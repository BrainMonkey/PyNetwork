import difflib
import sys

with open('PROD.txt', 'r') as PROD:
    with open('DR.txt', 'r') as DR:
        diff = difflib.ndiff(
            PROD.readlines(),
            DR.readlines(),
            #fromfile='hosts0',
            #tofile='hosts1',
        )
        for line in diff:
            #sys.stdout.write(line)
	    delta = ''.join(x[2:] for x in diff if x.startswith('- '))
	    print"The following config is in PROD but NOT DR:\n"
            print delta
