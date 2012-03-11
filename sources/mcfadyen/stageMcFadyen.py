import sys
sys.path.append("../../support")

import getopt
import shutil
import os

import patch

def stage():
    print '#### Staging McFadyen...'
    p = patch.Patcher()
    p.setup('sources/mcfadyen/usfm', 'sources/mcfadyen/patches', 'staging', 'cth')
    p.patch()
    

