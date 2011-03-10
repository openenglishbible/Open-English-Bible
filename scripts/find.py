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

def generatePatchForFind(find, replace, ignoreCase=False, plural=False):
    p = u''
    for b in books:
        print '     Looking in ' + b
        f = open('../patched/' + b + '.usfm', 'r')
        fc = unicode(f.read(), 'utf-8')
        f.close()
        
        found = findInBook(find, fc, replace, ignoreCase, plural)
        if len(found) > 0:        
            p = p + u'\nIn ' + b + u':\n'
            p = p + findInBook(find, fc, replace, ignoreCase, plural)
    return p
    
def findInBook(find, book, replace, ignoreCase=False, plural=False):
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
        if isMatch(book, i, find, ignoreCase):
            context = (u'    ' + str(c) + u':' + str(v)).ljust(12)
            p = p + u'    ; ' + book[i-20:i+80].replace(u'\n', u' ') + u'\n'
            p = p + context + find + u'  ->  ' + replace + u'\n'
            i = i + len(find)
        elif plural and isMatch(book, i, find + 's', ignoreCase):
            context = (u'    ' + str(c) + u':' + str(v)).ljust(12)
            p = p + u'    ; ' + book[i-20:i+80].replace(u'\n', u' ') + u'\n'
            p = p + context + find + u's  ->  ' + replace + u's\n'                
            i = i + len(find) + 1 
        i = i + 1
    return p
    
def isMatch(book, i, find, ignoreCase):
    if ignoreCase:
        return book[i:i+len(find)].lower() == find.lower() and isSeparator(book[i-1]) and isSeparator(book[i+len(find)])
    else: 
        return book[i:i+len(find)] == find and isSeparator(book[i-1]) and isSeparator(book[i+len(find)])
            
def isSeparator(c):
    s = u"""\n\t -.,!? —‘“”’;:()'"[]\\"""
    return s.find(c) != -1

def findElement(book, index):
    i = index
    while i < len(book) and not book[i].isspace():
        i = i + 1
    return (int(i), book[index:i])


def main(argv):
    print '#### Starting Find.'
    try:
        opts, args = getopt.getopt(argv, "inhf:p:r:", ["ignoreCase", "ignoreNumber", "help", "find=", "replace=", "patch="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    find = replace = patch = ''
    ignoreCase = plural = False
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-f", "--find"):
            find = arg
        elif opt in ("-p", "--patch"):
            patch = arg
        elif opt in ("-r", "--replace"):
            replace = arg
        elif opt in ("-i", "--ignoreCase"):
            ignoreCase = True
        elif opt in ("-n", "--ignoreNumber"):
            plural = True

    if find == '':
        usage()
    else:
        print '     Finding: "' + find + '"'
        p = generatePatchForFind(find, replace, ignoreCase, plural)

        print p
        if not patch == '':
            f = open(patch, 'w')
            f.write(p.encode('utf-8'))
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