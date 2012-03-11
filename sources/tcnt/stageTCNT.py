import sys
sys.path.append("../../support")

import getopt
import shutil
import os

import patch

def stage():
    print '#### Staging 20th Century New Testament...'
    p = patch.Patcher()
    p.setup('sources/tcnt/usfm', 'sources/tcnt/patches', 'staging', 'cth')
    p.patch()

