import sys
sys.path.append("support")

import getopt

import patch

def doPatch():
    # Create patched usfm
    print '#### Patching...'
    p = patch.Patcher()
    p.setup('source', 'patches', 'patched')
    p.patch()

def main(argv):
    print '#### Starting Build.'
    try:
        opts, args = getopt.getopt(argv, "hp", ["help", "patch"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-p", "--patch"):
            doPatch()
        else:
            usage()
    print '#### Finished.'

def usage():
    print """
        Open English Bible
        ------------------

        Build script.

        -h or --help for options
        -p or --patch to patch only
    """

if __name__ == "__main__":
    main(sys.argv[1:])