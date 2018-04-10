#!/usr/bin/env python
from os import path  #Importing two methods from os module
from optparse import OptionParser    #Imports the option parser module
import sys

###### OPTIONS and USAGE ######
parser = OptionParser(usage = """fastq_grabber.py -f FASTQ_FILE -l ID_LIST -o OUTPUT [-c -s SEPARATOR]

fastq_grabber.py - Outputs fastq sequences with IDs that exactly match
    (including the leading '@') the IDs present in a list. Note that for paired
    end reads your list of IDs will need a separate entry for each member of
    the pair. Use the -c flag to match just the first portion of a read ID.

                                       by
                                Kevin Weitemier
                                  April  2018

Copyright (c) 2013,2018  Kevin Weitemier.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. A copy of this license is available at <http://www.gnu.org/licenses/>.
Great effort has been taken to make this software perform its said
task, however, this software comes with ABSOLUTELY NO WARRANTY,
not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Input - A fastq file and a list of fastq IDs.""")
parser.add_option("-f", action="store", type="string", dest="fastqfile",
    help='Name of the fastq file. May be "-" for STDIN.', default="")
parser.add_option("-l", action="store", type="string", dest="listfile",
    help="Name of the list file", default="")
parser.add_option("-o", action="store", type="string", dest="outname",
    help='Name of the output file. May be "-" for STDOUT.', default="")
parser.add_option("-c", action="store_true", dest="header", default=False,
    help="Only match by the first column of the ID? (separator given by -s)")
parser.add_option("-s", action="store",
    type="string", dest="separator", default=" ",
    help="""When used with -c, delimitor for the first column of the ID. Default=" "[space].""")
(options, args) = parser.parse_args()

# Makes sure all filenames are given
if options.fastqfile == "":
    parser.error("Please include the fastq file using -f.")
if options.listfile == "":
    parser.error("Please include the list file using -l.")
if options.outname == "":
    parser.error("Please include and output filename using -o.")

###### OPENING INPUT/OUTPUT FILES ######
if path.isfile(options.outname) and options.outname != "-":
    parser.error("""The output filename exists. Please delete it first or \
choose a new name.""")
if options.fastqfile == "-":
    Infile2 = sys.stdin
else:
    Infile2 = open(options.fastqfile, 'r')
Infile1 = open(options.listfile, 'r')
if options.outname == "-":
    Outfile = sys.stdout
else:
    Outfile = open(options.outname, 'w')

# Get the list of bubbles
Line1 = Infile1.readline()
BubbleDict = {}
while Line1:
    Line1 = Line1.strip()
    BubbleDict[Line1] = []
    Line1 = Infile1.readline()

# Grab the matching bubbles
Line2 = Infile2.readline()
while Line2:
    if options.header:
        Fields = Line2.split(options.separator)
        TestNum = Fields[0]
    else:
        TestNum = Line2.strip()
    if TestNum in BubbleDict:
        Outfile.write("%s" % (Line2))
        Line2 = Infile2.readline()
        Outfile.write("%s" % (Line2))
        Line2 = Infile2.readline()
        Outfile.write("%s" % (Line2))
        Line2 = Infile2.readline()
        Outfile.write("%s" % (Line2))
        Line2 = Infile2.readline()
    else:
        Line2 = Infile2.readline()
        Line2 = Infile2.readline()
        Line2 = Infile2.readline()
        Line2 = Infile2.readline()

###### CLEANUP ######
Infile1.close()
Infile2.close()
Outfile.close()
###### EOF ######
