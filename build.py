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
    p.setup('staging/tcnt', 'patches/tcnt', 'patched/cth', 'cth')
    p.patch()

    p = patch.Patcher()
    p.setup('staging/tcnt', 'patches/tcnt', 'patched/us', 'us')
    p.patch()

    p = patch.Patcher()
    p.setup('staging/mcfadyen', 'patches/mcfadyen', 'patched/cth', 'cth')
    p.patch()

    p = patch.Patcher()
    p.setup('staging/mcfadyen', 'patches/mcfadyen', 'patched/us', 'us')
    p.patch()
    
    print '#### Finished.'

if __name__ == "__main__":
    main(sys.argv[1:])