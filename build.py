import sys
sys.path.append("support")

import getopt

import patch

def doPatch(spelling, subdir):
    # Create patched usfm
    print '#### Patching...'
    p = patch.Patcher()
    p.setup('source', 'patches', 'patched/' + subdir, spelling)
    p.patch()

def main(argv):
    print '#### Starting Build.'
    try:
        opts, args = getopt.getopt(argv, "hucb", ["help", "us", "cth", "both"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-u", "--us"):
            doPatch('us', 'us')
        elif opt in ("-c", "--cth"):
            doPatch('cth', 'cth')
        elif opt in ("-b", "--both"):
            doPatch('cth', 'cth')
            doPatch('us', 'us')
        else:
            usage()
    if opts == []: usage()
    print '#### Finished.'

def usage():
    print """
        Open English Bible
        ------------------

        Build script.

        -h or --help for options
        -u or --us to patch with US spelling
        -c or --cth to patch with Commonwealth spelling
        -b or --both to patch both spellings
    """

if __name__ == "__main__":
    main(sys.argv[1:])