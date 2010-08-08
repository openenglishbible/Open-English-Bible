# -*- coding: utf-8 -*-
#

import sys
import getopt
import difflib

books = [   'Matthew',
            'Mark',
            'Luke',
            'John',
            'Acts',
            'Romans',
            '1 Corinthians',
            '2 Corinthians',
            'Galatians',
            'Ephesians',
            'Philippians',
            'Colossians',
            '1 Thessalonians',
            '2 Thessalonians',
            '1 Timothy',
            '2 Timothy',
            'Titus',
            'Philemon',
            'Hebrews',
            'James',
            '1 Peter',
            '2 Peter',
            '1 John',
            '2 John',
            '3 John',
            'Jude',
            'Revelation']

def generatePatchForFind(find, replace):
    p = u''
    for b in books:
        print '     Looking in ' + b
        f = open('../source/' + b + '.usfm', 'r')
        fc = unicode(f.read(), 'utf-8')
        f.close()
        
        found = findInBook(find, fc, replace)
        if len(found) > 0:        
            p = p + u'\nIn ' + b + u':\n'
            p = p + findInBook(find, fc, replace)
    return p
    
def findInBook(find, book, replace):
    c = 1
    v = 1
    p = u''
    i = 0
    while i < len(book):
        if book[i:i+3] == u'\\c ':
            i = i + 3
            (i, c) = findElement(book, i)
        if book[i:i+3] == u'\\v ':
            i = i + 3
            (i, v) = findElement(book, i)
        if book[i:i+len(find)] == find and isSeparator(book[i-1]) and isSeparator(book[i+len(find)]):
            context = (u'    ' + str(c) + u':' + str(v)).ljust(12)
            p = p + context + find + u'  ->  ' + replace + u'\n'
            i = i + len(find)
        i = i + 1
    return p
            
def isSeparator(c):
    s = u"""\n\t -.,!? —‘“”’;:()'"[]"""
    return s.find(c) != -1

def findElement(book, index):
    i = index
    while i < len(book) and not book[i].isspace():
        i = i + 1
    return (int(i), book[index:i])


def main(argv):
    print '#### Starting Find.'
    try:
        opts, args = getopt.getopt(argv, "hf:p:r:", ["help", "find=", "replace=", "patch="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    find = replace = patch = ''
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-f", "--find"):
            find = arg
        elif opt in ("-p", "--patch"):
            patch = arg
        elif opt in ("-r", "--replace"):
            replace = arg

    if find == '':
        usage()
    else:
        print '     Finding: "' + find + '"'
        p = generatePatchForFind(find, replace)

        if patch == '':
            print p
        else:
            f = open(patch, 'w')
            f.write(p)
            f.close()

    print '#### Finished.'


def usage():
    print """
        Open English Bible
        ------------------

        Finder / Patch creator.

        -h or --help for options
        -f or --find for sequence to match
        -r or --replace for sequence to replace
        -p or --patch for patch name (stdout if omitted)
    """

if __name__ == "__main__":
    main(sys.argv[1:])