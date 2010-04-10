import sys
sys.path.append("support")

from subprocess import Popen, PIPE
import getopt

import patch
import texise
import htmlise

def runscript(c, prefix=''):
    pp = Popen(c, shell=True, stdout=PIPE)
    for ln in pp.stdout:
        print prefix + ln[:-1]

def setup():
    c = """
    cd thirdparty
    rm -rf context
    mkdir context
    cd context
    curl -o first-setup.sh http://minimals.contextgarden.net/setup/first-setup.sh
    sh ./first-setup.sh
    . ./tex/setuptex
    """
    runscript(c)


def doPatch():
    # Create patched usfm
    print '#### Patching...'
    p = patch.Patcher()
    p.setup('source', 'patches', 'patched')
    p.patch()

def buildAll():

    buildPDF()
    buildWeb()

def buildPDF():

    print '#### Building PDF...'

    # Convert to ConTeXt
    print '     Converting to TeX...'
    c = texise.TransformToContext()
    c.setupAndRun('patched', 'preface', 'working/tex')

    # Build PDF
    print '     Building PDF..'
    c = """. ./thirdparty/context/tex/setuptex ; cd working/tex-working; rm * ; context ../tex/Bible.tex; cp *.pdf ../../built/"""
    runscript(c, '     ')

def buildWeb():
    # Convert to HTML
    print '#### Building HTML...'
    c = htmlise.TransformToHTML()
    c.setupAndRun('patched', 'preface', 'built')

def main(argv):
    print '#### Starting Build.'
    try:
        opts, args = getopt.getopt(argv, "shawpg:d", ["setup", "help", "all", "web", "patch", "grammar="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-s", "--setup"):
            setup()
        elif opt in ("-a", "--all"):
            doPatch()
            buildAll()
        elif opt in ("-w", "--web"):
            doPatch()
            buildWeb()
        elif opt in ("-p", "--patch"):
            doPatch()
            buildWeb()
    print '#### Finished.'


def usage():
    print """
        Open English Bible
        ------------------

        Build script.

        -h or --help for options
        -s or --setup to setup up environment and load third party support
        -a or --all to build all books in all targets
        -w or --web to build web version only
        -p or --patch to patch only
    """

if __name__ == "__main__":
    main(sys.argv[1:])