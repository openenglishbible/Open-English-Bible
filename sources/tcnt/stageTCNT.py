import sys
sys.path.append("../../support")

import getopt
import shutil
import os

import patch

def stage():
    print '#### Staging 20th Century New Testament...'
    p = patch.Patcher()
    p.setup('sources/tcnt/usfm', 'sources/tcnt/patches', 'staging/cth', 'cth', swapQuotes=True) # Get into proper Cth quotes
    p.patch()

    p = patch.Patcher()
    p.setup('sources/tcnt/usfm', 'sources/tcnt/patches', 'staging/us', 'us', swapQuotes=False) # Get into proper US quotes
    p.patch()
