import sys
sys.path.append("support")

import getopt
import shutil
import os

import patch

def main(argv):
    print '#### Starting Build.'
        
    print '   # Patching...'
    p = patch.Patcher()
    p.setup('staging/tcnt', 'patches/tcnt', 'final-usfm/cth', 'cth')
    p.patch()

    p = patch.Patcher()
    p.setup('staging/tcnt', 'patches/tcnt', 'final-usfm/us', 'us')
    p.patch()

    p = patch.Patcher()
    p.setup('staging/mcfadyen', 'patches/mcfadyen', 'final-usfm/cth', 'cth')
    p.patch()

    p = patch.Patcher()
    p.setup('staging/mcfadyen', 'patches/mcfadyen', 'final-usfm/us', 'us')
    p.patch()
    
    p = patch.Patcher()
    p.setup('staging/kent', 'patches/kent', 'final-usfm/cth', 'cth')
    p.patch()

    p = patch.Patcher()
    p.setup('staging/kent', 'patches/kent', 'final-usfm/us', 'us')
    p.patch()
    
    print '#### Finished.'

if __name__ == "__main__":
    main(sys.argv[1:])