import sys, getopt
from collections import defaultdict
from pprint import pprint

def separate(iname, oname1, oname2):
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
        sline = line.strip().split(' ')
        ofile1.write(sline[0] + '\n')
        ofile2.write(sline[1] + '\n')

def main(argv):
    iname = ''
    out1 = ''
    out2 = ''
    #oname = ''

    try:
        opts, args = getopt.getopt(argv, 'i:o:p:', ["input=", "outout1=", "output2="])
    except getopt.GetoptError:
        print 'Usage: filter.py -i <inputfile> -o <outfile1> -op <outfile2>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i', '--input'):
            iname = arg
        elif opt in ('-o', '--output1'):
            out1 = arg
        elif opt in ('-p', '--output2'):
            out2 = arg

    separate(iname, out1, out2)


if __name__ == "__main__":
    main(sys.argv[1:])
