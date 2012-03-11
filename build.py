import sys
sys.path.append("support")
sys.path.append("sources/tcnt")
sys.path.append("sources/mcfadyen")
sys.path.append("sources/kent")

import getopt
import shutil
import os

import patch
import stageTCNT
import stageMcFadyen
import stageKent

def main(argv):
    print '#### Staging...'
        
    stageTCNT.stage()
    stageMcFadyen.stage()
    stageKent.stage()
    
    print '#### Final Patching...'

    p = patch.Patcher()
    p.setup('staging/', 'patches/', 'final-usfm/cth', 'cth')
    p.patch()

    p = patch.Patcher()
    p.setup('staging/', 'patches/', 'final-usfm/us', 'us')
    p.patch()
   
    print '#### Finished.'

if __name__ == "__main__":
    main(sys.argv[1:])