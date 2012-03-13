import sys
sys.path.append("../../support")

import getopt
import shutil
import os

import patch

def stage():
    print '#### Staging McFadyen...'
    
    #So Crosswire doesn't barf
    f = open('sources/mcfadyen/usfm/19-Psalms.usfm')
    s  = unicode(f.read(), 'utf-8')
    f.close()
    
    s = s.replace(u'\\v ', u'\n\\v ')
    
    f = open('sources/mcfadyen/tmp/19-Psalms.usfm', 'w')
    f.write(s.encode('utf-8'))
    f.close()
    
    p = patch.Patcher()
    p.setup('sources/mcfadyen/tmp', 'sources/mcfadyen/patches', 'staging', 'cth')
    p.patch()
    

