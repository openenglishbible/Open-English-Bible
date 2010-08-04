# -*- coding: utf-8 -*-
#

import os
import parseUsfm

class HTMLPrinter(object):
    def __init__(self):
        pass

    def renderID(self, token):      return u""
    def renderIDE(self, token):     return u""
    def renderH(self, token):       return u'<h1>' + token.value + u'</h1>'
    def renderMT(self, token):      return u'<h2>' + token.value + u'</h2>'
    def renderMS(self, token):      return u'<h3>' + token.value + u'</h3>'
    def renderMS2(self, token):     return u'<h4>' + token.value + u'</h4>'
    def renderP(self, token):       return u'<p />'
    def renderS(self, token):       return u'<p /><p align="Center">—</p>'
    def renderC(self, token):       return u'<h1>' + token.value + u'</h1>'
    def renderV(self, token):       return u'<b>' + token.value + u'</b>'
    def renderWJS(self, token):     return u""
    def renderWJE(self, token):     return u""
    def renderTEXT(self, token):    return u" " + token.value + u" "
    def renderQ(self, token):       return u''
    def renderQ1(self, token):      return u''
    def renderQ2(self, token):      return u''
    def renderQ3(self, token):      return u''
    def renderNB(self, token):      return u''
    def renderQTS(self, token):      return u''
    def renderQTE(self, token):      return u''
    def renderFS(self, token):      return u''
    def renderFE(self, token):      return u''
    def renderIS(self, token):      return u'<i>'
    def renderIE(self, token):      return u'</i>'

class TransformToHTML(object):

    def translateBook(self, name):

        f = open(self.patchedDir + '/' + name + '.usfm')
        fc = unicode(f.read(), 'utf-8')
        f.close()

        print '        > ' + name
        tokens = parseUsfm.parseString(fc)

        s = u''
        tp = HTMLPrinter()
        for t in tokens: s = s + t.renderOn(tp)
        return s

    def saveAll(self, allBooks):

        s = u"""
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
	        <head>
		        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
		    </head>
		    <body>""" + allBooks + "</body></html>"


        f = open(self.outputDir + '/Bible.html', 'w')
        f.write(s.encode('utf-8'))
        f.close()

    def setupAndRun(self, patchedDir, prefaceDir, outputDir):
        self.patchedDir = patchedDir
        self.prefaceDir = prefaceDir
        self.outputDir = outputDir

        # Setup list of patches and books to use
        #
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
        #preface = unicode(open(self.prefaceDir + '/preface.tex').read(), 'utf-8').strip()
        #bookTex = preface
        bookTex = u''
        for book in books:
            bookTex = bookTex + self.translateBook(book)
        self.saveAll(bookTex)