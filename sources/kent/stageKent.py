# -*- coding: utf-8 -*-
#

import sys
sys.path.append("../../support")

import getopt
import shutil
import os

def listDirectory(directory, spelling):                                        
    allfiles = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.usfm'):
                p = os.path.join(root, f)
                allfiles.append(p)
    allfiles.sort()
    return allfiles

def stage():
    print '#### Staging Kent...'
    
    for fn in os.listdir('sources/kent/'):
        if fn[-5:] == '.usfm':
            f = open('sources/kent/' + fn)
            c = f.read().decode('utf-8-sig')
            f.close()
            u = u''
            ignore = False
            for char in c:
                if char == u'>':
                    ignore = False
                elif ignore:
                    pass
                elif char == '<':
                    ignore = True
                elif char == u'[' or char == u']' or char == u'{' or char == u'}':
                    pass
                else:
                    u = u + char
            f = open('staging/' + fn, 'w')
            f.write(u.encode('utf-8'))
            f.close
        


    

