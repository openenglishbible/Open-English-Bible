#/usr/bin/python

import os, glob, re, codecs

for ver in ["cth", "us"]:

    path = "./" + ver + "/"
    for inf in glob.glob(os.path.join(path, '*.usfm')):
        print "processing " + inf
    
        sfText = codecs.open(inf, encoding='utf-8').read()

        dest = "./dest"+ver+"/"
        try:
            os.mkdir(dest)
        except OSError:
            pass

        outfStr = inf
        bookHash = {'Psalms': '19', 'Matthew': '40', 'Mark': '41', 'Luke': '42', 'John': '43', 'Acts': '44', 'Romans': '45', '1 Corinthians': '46', '2 Corinthians': '47', 'Galatians': '48', 'Ephesians': '49', 'Philippians': '50', 'Colossians': '51', '1 Thessalonians': '52', '2 Thessalonians': '53', '1 Timothy': '54', '2 Timothy': '55', 'Titus': '56', 'Philemon': '57', 'Hebrews': '58', 'James': '59', '1 Peter': '60', '2 Peter': '61', '1 John': '62', '2 John': '63', '3 John': '64', 'Jude': '65', 'Revelation': '66'}
        # this prepends a book number, so that usfm2osis.pl gets the books in the correct order
        outfStr = outfStr[:len(ver)+3] + bookHash[outfStr[len(ver)+3:-5]] + "-" + outfStr[len(ver)+3:]

        outf = codecs.open(outfStr.replace(path, dest, 1), encoding='utf-8', mode='w')

        # invert order of \v # \p, when they occur in that order and add newline after \p
        sfText = re.sub(r'(\\v\b\s+\d+\b)(\\p\b)', r'\2\n\1', sfText)

        # \p, \q, and \v are only expected at the beginning of a line
        sfText = re.sub(r'([^\n])(\\[pqv])', r'\1\n\2', sfText)

        # section headings (\s, \ms) should be within a chapter
        sfText = re.sub(r'((\\m?s\d?\b[^\n]*\n+(\\rem\b[^\n]*\n+)?|\\q\s*\n+)+)(\\c\b[^\n]*\n)', r'\4\1', sfText)

        # \it is used in USFM for italics
        sfText = re.sub(r'\\i\b', '\\it', sfText)
    

        # strip leading & trailing whitespace, terminate with newline
        sfText = re.sub(r'\s*\n\s*', r'\n', sfText)
        sfText += '\n'

        outf.write(sfText)
