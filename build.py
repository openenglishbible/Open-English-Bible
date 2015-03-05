# -*- coding: utf-8 -*-
#

import sys
sys.path.append("support")

import getopt
import shutil
import os
import re
import ConfigParser
import itertools

import versions    
import regressionTesting

def tagCombinations(dir):
    config = ConfigParser.RawConfigParser()
    tags = []
    try:
        config.read(dir + '/tags.db')
    except:
        print 'Could not read tags file'
        sys.exit(0)
    for s in config.sections():
        tags.append(config.options(s))
    return list(itertools.product(*tags))

def saveIfDifferent(dir, fn, contents):
    try:
        f = open(dir + '/' + fn)
        b = unicode(f.read(), 'utf-8')
        f.close()
    except:
        b = ''
    
    if not contents == b:
        print '>>>> ' + fn
        f = open(dir + '/' + fn, 'w')
        f.write(contents.encode('utf-8'))
        f.close()
    else:
        print '     ' + fn

def stage(src, to, tags):
    print '     ' + str(tags)
    for fn in os.listdir(src + '/'):
        if fn[-8:] == '.usfm.db':
            
            f = open(src + '/' + fn)
            b  = unicode(f.read(), 'utf-8')
            f.close()
            
            s = versions.render(b, tags)
            
            #To get quotes right to Cth versions, swap “”‘’ to get US and Cth OK
            if 'cth' in tags:
                s = s.replace(u'“', u'@leftdoublequote@')
                s = s.replace(u'”', u'@rightdoublequote@')
                s = s.replace(u'‘', u'@leftsinglequote@')
                s = s.replace(u'’', u'@rightsinglequote@')
                s = s.replace(u'@leftdoublequote@', u'‘')
                s = s.replace(u'@rightdoublequote@', u'’')
                s = s.replace(u'@leftsinglequote@', u'“')
                s = s.replace(u'@rightsinglequote@', u'”')
                
            # Clean up line endings so Crosswire's sofware doesn't barf
            # strip leading & trailing whitespace, terminate with newline
            s = s.replace(u'\\v ', u'\n\\v ')
            s = re.sub(r'\s*\n\s*', r'\n', s)
    
            saveIfDifferent(to, fn[:-3], s)
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "has:b:t:", ["help", "all", "source=", "build=", "tags="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    source = build = tags = ''
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-s", "--source"):
            source = arg
        elif opt in ("-b", "--build"):
            build = arg
        elif opt in ("-t", "--tags"):
            tags = arg.split('-')
        elif opt in ("-a", "--all"):
            doAll = True
            
    if doAll == True:       
        for tc in tagCombinations(source):
            print '#### Staging...'
            d = build + '-'.join(tc) 
            if not os.path.exists(d):
                os.makedirs(d)
            stage(source, d,  tc)
            regressionTesting.Tester().test(d)
    else:    
        print '#### Staging...'
        stage(source, build,  tags)
           
        print '#### Regression Testing...'
        regressionTesting.Tester().test(build)
    
def usage():
    print """
        Open English Bible
        ------------------

        USFM Builder

        -h or --help for these options
        -s or --source for directory of source .usfm.db files
        -b or --build for directory of built .usfm files
        -t or --tags for hyphen separated list of tags
        -a or --all to build all tag combinations
    """

if __name__ == "__main__":
    main(sys.argv[1:])