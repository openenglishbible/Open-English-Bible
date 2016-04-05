# -*- coding: utf-8 -*-
#

import os
import re

def pos(usfm, index):
    x = usfm[:index].count('\n')
    return x

class Tester(object):
    def loadBooks(self, path):
        books = {}
        dirList=os.listdir(path)
        print '     Checking ' + path
        #print '     Loading all Usfm files from ' + path
        for fname in dirList:
          try:
              f = open(path + '/' + fname,'U') # U handles line endings
              usfm = f.read().decode('utf-8-sig')
              books[fname] = usfm
              #print '     Loaded ' + fname
              f.close()
          except:
              if not fname == '.DS_Store':
                  print '     - Couldn\'t open ' + fname
        #print '     Finished loading'
        return books
    
    def test(self, dir):
        books = self.loadBooks(dir)
        for b in books:
            self.testMalformedCodes(b, books[b])
            self.testDuplicates(b, books[b])
            self.testMisplacedSpaces(b, books[b])
            self.testMissingSpaces(b, books[b])
            self.testExtraSpaces(b, books[b])
            self.testParas(b, books[b])
            self.testPoetry(b, books[b])
            self.testSectionHeaders(b, books[b])
            self.testWJ(b, books[b])
            self.testB(b, books[b])
            self.testM(b, books[b])
            self.testDash(b, books[b])
            self.testApostrophe(b, books[b])
            self.testNesting(b, books[b])
            self.testFootnotes(b, books[b])

    def testMalformedCodes(self, b, u):
        w = u.split(u' \n\t.,:?;\'\"')
        self.checkForCode('sea', w)
        
    def checkForCode(self, c, w):
        if c in w:  print '     - Malformed code? \'' + c + '\' in ' + u[:50]
    
    def testDuplicates(self, b, u):
        for c in u':.,\'"‘’“”':
            if c + c in u:
                print 'Duplicate "' + c + '" in ' + b
                
    def testExtraSpaces(self, b, u):
        for i, l in enumerate(u.split('\n')):
            if not l == '' and l[-1] == ' ':
                print 'Extra space on line: ' + str(i +1) + ' of ' + b


    def testMisplacedSpaces(self, b, u):
        for i, l in enumerate(u.split('\n')):
            if u' .' in l:
                print 'Misplaced ~. on line: ' + str(i +1) + ' of ' + b
            if u' ,' in l:
                print 'Misplaced ~, on line: ' + str(i +1) + ' of ' + b
            if u' ;' in l:
                print 'Misplaced ~; on line: ' + str(i +1) + ' of ' + b
                
    def testMissingSpaces(self, b, u):
        t = u'.,;:'
        for i, c in enumerate(u):
            if c in t: 
                if i < len(u) - 1:
                    if not u[i+1] in u' \n\\”’)0123456789':
                        print 'Missing space in ' + b + ' at ' + str(i)
                        
    def testParas(self, b, u):
        """
        When a paragraph and verse start together, always put the paragraph marker before the verse marker.
        (If there is no actual paragraph starting there, use \nb.)
        """
        if u'\\p\n\\c' in u:
            print 'Misplaced Paragraph marker against chapter in: ' + b
        rx = re.compile('\\\\v [0-9]+\\n\\\\p')
        if not rx.search(u) == None:
            print 'Misplaced Paragraph marker against verse in: ' + b
            
    def testSectionHeaders(self, b, u):
        """
        Section headers associated with a chapter should appear at the beginning of that chapter rather than the end of it.
        """
        i = 0
        while i < len(u):
            i = u.find(r'\s', i)
            if i == -1:
                return
            c = u.find(r'\c', i)        
            if c == -1:
                return
            if c - i < 50:
                print 'Misplaced Section Header against chapter in: ' + b
            i = c

    def testWJ(self, b, u):
        """
        Character styles cannot cross paragraph or verse boundaries, but must be stopped and restarted at those points. This is significant with \wj ...\wj*.
Character styles (like \wj ...\wj*) cannot continue through footnotes, but must be stopped and restarted around the footnote.
        """
        i = 0
        while i < len(u):
            i = u.find(r'\wj ', i)
            if i == -1:
                return
            f = u.find(r'\f', i)        
            if f== -1:
                return
            e = u.find(r'\wj*', i)        
            if e == -1:
                return
            if f < e:
                print 'Interrupted \wj in: ' + b
            i = e
            
    def testB(self, b, u):
        """
        \b cannot have text content.
        """
        if not u.find(r'\b ') == -1: print '\\b tag with text content in: ' + b
        
    def testM(self, b, u):
        """
        \m cannot be empty of text content.
        """
        i = 0
        while i < len(u):
            i = u.find('\\m\n', i)
            if i == -1: return
            if not u[i+3] == '\\': print '\\m tag with no text content in: ' + b
            i = i + 3

    def testDash(self, b, u):
        """
        Standard is n-dash with surrounding space
        """
        i = u.find(u'—')
        if not i == -1:
            print 'm-dash in ' + b + ' at position ' + str(pos(u,i))
        i2 = u.find(u' - ')
        if not i2 == -1:
            print 'hyphen as n-dash in ' + b + ' at  ' + str(pos(u,i2))
        i3 = u.find(u' -')
        if not i3 == -1:
            print 'hyphen as n-dash in ' + b + ' at  ' + str(pos(u,i3))
        i4 = u.find(u'-\n')
        if not i4 == -1:
            print 'hyphen as n-dash in ' + b + ' at  ' + str(pos(u,i4))
        rx = re.compile(r'[^\s]–')
        if not rx.search(u) == None:
            print 'n-dash without prior space in: ' + b
        rx = re.compile(r'–[^\s]')
        if not rx.search(u) == None:
            print 'n-dash without subsequent space in: ' + b

    def testApostrophe(self, b, u):
        """
        Simple ascii apostrophe's shouldn't appear in final product
        """
        i = u.find(u'\'')
        if not i == -1:
            print 'apostophe in ' + b + ' at line ' + str(pos(u,i))

    def testNesting(self, b, u):
        """
        \em I am the \+nd Lord\+nd*\em*
        """
        rx = re.compile(r'\\em[^\*][^\\]+\\nd')
        if not rx.search(u) == None:
            print 'Possible need for nested markup in: ' + b

    def testPoetry(self, b, u):
        """
        When a poetic line and verse start together, always put the poetry marker before the verse marker.
        """
        if u'\\q\n\\c' in u:
            print 'Misplaced Poetry marker against chapter in: ' + b
        rx = re.compile('\\\\v [0-9]+\\n\\\\q')
        if not rx.search(u) == None:
            print 'Misplaced poetry marker against verse in: ' + b

    def testFootnotes(self, b, u):
        """
        Footnotes should have back reference
        """
        rx = re.compile(r'\\f \+ [^\\][^f][^r]')
        if not rx.search(u) == None:
            print 'Footnote without back reference in: ' + b
