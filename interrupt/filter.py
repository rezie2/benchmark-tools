from __future__ import division
import sys, getopt
from collections import defaultdict
from pprint import pprint
from decimal import *

def filter(iname, maximum, minimum, multiple):
    MAX = int(maximum)
    MIN = int(minimum)
    MULT = int(multiple)
    BINS = MAX // MULT
    ranges = []
    ftrd = defaultdict(list)

    #getcontext().prec = 2

    print "max is %d min is %d mult is %d" % (int(MAX), int(MIN), int(MULT))
    print "There are %d bins" % BINS
    for i in range(1, BINS+1):
        ranges.append(MULT * i)

    try:
        ifile = open(iname)
    except IOError as e:
        print "Error opening input file"
        sys.exit()

    try:
        outputname = iname.rstrip('.txt')+"out"+str(MIN)+"-"+str(MAX)+"-"+str(MULT)+".txt"
        ofile = open(outputname, 'w+')
    except IOError as e:
        print "Error opening outputfile"
        sys.exit()
    
    for snum in ifile:
        if int(snum) > MAX or int(snum) < MIN:
            continue
        for index in ranges:
            if int(snum) < int(index):
                ftrd[index].append(int(snum))
                break

    ofile.write("## MAX " + str(MAX) + " MIN " + str(MIN) + " MULT " + str(MULT) + "\n")
    for k in sorted(ftrd.iterkeys()):
        #temp = int(k) / int(MULT)
        ofile.write(str((Decimal(k) / Decimal(3300))) + ' ')
        #ofile.write(str(int(k)//MULT) + ' ')
        ofile.write(str(len(ftrd[k])) + "\n")

    ofile.close()
    ifile.close()

def main(argv):
    iname = ''
    #oname = ''

    try:
        opts, args = getopt.getopt(argv, 'i:m:n:u:', ["input=", "max=", "min=", "multiple="])
    except getopt.GetoptError:
        print 'Usage: filter.py -i <inputfile> -o <outputfile> \
            -m <max> -n <min> -u <multiple>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i', '--input'):
            iname = arg
        #elif opt in ('-o', '--output'):
        #    oname = arg
        elif opt in ('-m', '--max'):
            maximum = int(arg)
        elif opt in ('-n', '--min'):
            minimum = int(arg)
        elif opt in ('-u', '--multiple'):
            multiple = int(arg)

    filter(iname, maximum, minimum, multiple)


if __name__ == "__main__":
    main(sys.argv[1:])
