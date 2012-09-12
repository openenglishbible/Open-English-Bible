# -*- coding: utf-8 -*-
#

import sys
sys.path.append("../../support")

import getopt
import shutil
import os

import versions    


def stage():
    print '#### Staging McFadyen...'
    
    for fn in os.listdir('sources/mcfadyen/'):
        if fn[-8:] == '.usfm.db':
            
            f = open('sources/mcfadyen/' + fn)
            b  = unicode(f.read(), 'utf-8')
            f.close()
            
            s = b
            s = versions.render(s, ['neut','cth','oeb'])
            
            #So Crosswire doesn't barf
            s = s.replace(u'\\v ', u'\n\\v ')
    
            f = open('staging/cth/' + fn[:-3], 'w')
            f.write(s.encode('utf-8'))
            f.close()
    
            s = b
            s = versions.render(s, ['neut','us','oeb'])
            
            #So Crosswire doesn't barf
            s = s.replace(u'\\v ', u'\n\\v ')
    
            f = open('staging/us/' + fn[:-3], 'w')
            f.write(s.encode('utf-8'))
            f.close()

