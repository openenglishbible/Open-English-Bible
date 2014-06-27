#!/usr/bin/env python

#
#
#   QUICK AND DIRTY FILTER TO CLEAN USFM TO TEXT
#
#   eg cat file | clean.py
#

import sys, re

for line in sys.stdin:
    l = line
    l = l.replace("\\p ", "")
    
    l = re.compile(r'(\\v [0-9]+)').sub('', l)
    l = re.compile(r'(\\c [0-9]+)').sub('', l)
    
    for t in ['id', 'ide', 'h', 'mt2' , 'mt' , 'rem', 's', 'ms']:
        if l.find("\\" + t) >= 0: 
            l = ''

    if l == '\n': l = ''
    if not l == '': print l
    