# -*- coding: utf-8 -*-
#

import sys
import getopt
import difflib


def nextWord(aString, start):
    s = u''
    i = start
    while i < len(aString) and not (aString[i] == u' ' or aString[i] == u'\n'):
        s = s + aString[i]
        i = i + 1
    return (i, s)

def compare(sbefore, safter):
    i = 0
    while i < len(sbefore) and i < len(safter) and sbefore[i] == safter[i]: i = i + 1
    i2 = 0
    while len(sbefore) - i2 > i and len(safter) - i2 > i and sbefore[-i2] == safter[-i2]:
        i2 = i2 + 1

    while not isBreak(sbefore[i]): i = i - 1
    while not isBreak(sbefore[-i2]): i2 = i2 - 1
    i2 = i2 + 1
    while not isBreak(safter[-i2]): i2 = i2 - 1
    #i2 = i2 - 1
    return (sbefore[i:-i2], safter[i:-i2])

def isBreak(s):
    for c in u"""\n\t -.,!? —‘“”’;:()'"[]\\""":
        if c == s: return True
    return False

# input string
def parseString( aString ):
    t = []
    s = ''
    i = 0
    while i < len(aString):
        if aString[i] == u'\\' and (aString[i+1] == u'c' or aString[i+1] == u'v'):
            t.append(s)
            s = u'\\' + aString[i+1] + u' '
            i = i + 3
            (i, ts) = nextWord(aString, i)
            t.append(s + ts)
            s = u''
        else:
            s = s + aString[i]
            i = i + 1
    t.append(s)
    return t


def main(argv):
    print '#### Starting Build.'
    try:
        opts, args = getopt.getopt(argv, "hb:a:p:", ["help", "before=", "after=", "patch="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    before = after = patch = ''
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-b", "--before"):
            before = arg
        elif opt in ("-a", "--after"):
            after = arg
        elif opt in ("-p", "--patch"):
            patch = arg

    if before == '' or after == '' or patch == '':
        usage()
    else:
        # Breaks into \v and \c markers, and the strings between them
        f = open(before)
        b = unicode(f.read(), 'utf-8')
        f.close()
        b = parseString(b)

        # Breaks into \v and \c markers, and the strings between them
        f = open(after)
        a = unicode(f.read(), 'utf-8')
        f.close()
        a = parseString(a)

        i = 0
        c = 0
        v = 0
        p = ''
        while i < len(b):
            # Update current place
            if b[i][:2] == u'\c':
                c = int(b[i][3:])
                if not c == int(a[i][3:]):
                    print 'Chapter ' + b[i][3:] + ' != ' + a[i][3:]
                    sys.exit()
            if b[i][:2] == u'\\v':
                v = int(b[i][3:])
                if not v == int(a[i][3:]):
                    print 'Chapter ' + str(c) + ' : ' + b[i][3:] + ' != ' + a[i][3:]
                    sys.exit()
            # Otherwise, do compare
            if not a[i] == b[i]:
                # print '------------------\n' + b[i] + '\n-\n' + a[i]
                (subb, suba) = compare(b[i], a[i])
                p = p + str(c) + u':' + str(v) + u'  ' + subb.replace(u'\n', u'~') + u' -> ' + suba.replace(u'\n', u'~') + u'\n'
            i = i + 1

        f = open(patch, 'w')
        f.write(p.encode('utf-8'))
        f.close()

    print '#### Finished.'


def usage():
    print """
        Open English Bible
        ------------------

        Diff / Patch creator.

        -h or --help for options
        -b or --before for file before changes
        -a or --after for file after change
        -p or --patch for patch name
    """

if __name__ == "__main__":
    main(sys.argv[1:])