import sys, getopt, re
from collections import defaultdict
from pprint import pprint

def separate(iname, oname1, oname2):
    ftrd = defaultdict(list)

    try:
        ifile = open(iname)
    except IOError as e:
        print "Error opening input file"
        sys.exit()
    try:
        ofile1 = open(oname1, "w+")
    except IOError as e:
        print "Error opening outputfile1"
        sys.exit()
    try:
        ofile2 = open(oname2, "w+")
    except IOError as e:
        print "Error opening outputfile2"
        sys.exit()
    
    for line in ifile:
        match = re.search(r'\(([0-9]+)\) \[([0-9]+)\]', line)
        if match:
            ofile1.write(match.group(1) + "\n")
            ofile2.write(match.group(2) + "\n")

def main(argv):
    iname = ''
    out1 = ''
    out2 = ''

    try:
        opts, args = getopt.getopt(argv, 'i:t:d:', ["input=", "outout1=", "output2="])
    except getopt.GetoptError:
        print 'Usage: filter.py -i <inputfile> -t <outfile1> -d <outfile2>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i', '--input'):
            iname = arg
        elif opt in ('-t', '--output1'):
            out1 = arg
        elif opt in ('-d', '--output2'):
            out2 = arg

    print out1 + " " + out2

    separate(iname, out1, out2)

if __name__ == "__main__":
    main(sys.argv[1:])
