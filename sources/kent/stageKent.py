# -*- coding: utf-8 -*-
#

import sys
sys.path.append("../../support")

import getopt
import shutil
import os

import versions    


def stage():
    print '#### Staging Kent...'
    
    for fn in os.listdir('sources/kent/'):
        if fn[-8:] == '.usfm.db':
            
            f = open('sources/kent/' + fn)
            b  = unicode(f.read(), 'utf-8')
            f.close()
            
            s = b
            s = versions.render(s, ['oeb','neut','cth','nrsv', 'lord'])
            
            #To get quotes right to Cth versions, swap “”‘’ to get US and Cth OK
            s = s.replace(u'“', u'@leftdoublequote@')
            s = s.replace(u'”', u'@rightdoublequote@')
            s = s.replace(u'‘', u'@leftsinglequote@')
            s = s.replace(u'’', u'@rightsinglequote@')
            s = s.replace(u'@leftdoublequote@', u'‘')
            s = s.replace(u'@rightdoublequote@', u'’')
            s = s.replace(u'@leftsinglequote@', u'“')
            s = s.replace(u'@rightsinglequote@', u'”')
            
            #So Crosswire doesn't barf
            s = s.replace(u'\\v ', u'\n\\v ')
    
            f = open('staging/cth/' + fn[:-3], 'w')
            f.write(s.encode('utf-8'))
            f.close()
    
            s = b
            s = versions.render(s, ['oeb','neut','us','nrsv', 'lord'])
            
            #So Crosswire doesn't barf
            s = s.replace(u'\\v ', u'\n\\v ')
    
            f = open('staging/us/' + fn[:-3], 'w')
            f.write(s.encode('utf-8'))
            f.close()

