# -*- coding: utf-8 -*-
#

import os
import commands
import sys

def listDirectory(directory, spelling):                                        
    allfiles = []
 
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.patch'):
                p = os.path.join(root, f)
                if spelling == 'us':
                    allfiles.append(p)
                elif not 'us-spelling' in p:
                    allfiles.append(p)
                    
    allfiles.sort()
    return allfiles

class Patcher(object):

    def setup(self, sourceDir, patchDir, outputDir, spelling):
        self.sourceDir = sourceDir
        self.patchDir = patchDir
        self.outputDir = outputDir
        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)
        self.patches = listDirectory(self.patchDir, spelling)
        self.versesPatched = []
        self.books = os.listdir(self.sourceDir)
        self.books = [b[:-5] for b in self.books if b[-5:] == '.usfm']
    
    def patch(self):
        self.debugPrint( 'Starting to Patch' )
        for b in self.books:
            self.patchBook(b)
        
    def patchBook(self, book):
        self.debugPrint( book )
        bookname = self.sourceDir + '/' + book + '.usfm'
        f = open(bookname)
        s = unicode(f.read(), 'utf-8')
        f.close()
        
        for p in self.patches:
            s = self.applyPatchToBook(book, s, p)
        
        bookname = self.outputDir + '/' + book + '.usfm'
        f = open(bookname, 'w')
        f.write(s.encode('utf-8'))
        f.close()

    def findPatch(self, s, b, st, en):
        i = st
        while i < en:
            x = s.find(b, i, en)
            if x == -1: return -1
            # Our patch must either be surrounded by separtors, or must  itself be top or tailed with a separator
            if (self.isSeparator(s[x-1]) or self.isSeparator(b[0])) and (self.isSeparator(s[x+len(b)] or self.isSeparator(b[-1]))): return x
            i = x + 1
        return -1
        
    def applyPatchToBook(self, book, s, patch):
        # Only warn for collisions between patches
        patchesAlreadyApplied = []
        
        self.debugPrint('    ' + patch)

        f = open(patch)
        p = unicode(f.read(), 'utf-8').strip()
        f.close()

        lines = p.strip().splitlines()
        lines = [line for line in lines if not (line.isspace() or line == '')]  # Remove empty lines
        lines = [line for line in lines if (not line.lstrip()[0] == ';')]                # Remove comments
        
        # Forward to appropriate place
        i = 0
        while i < len(lines) and not book == lines[i].strip()[3:-1]: i = i + 1
        i = i + 1
        
        while i < len(lines) and (not (lines[i].strip()[:3] == 'In ')):
            x = lines[i].strip().split(None, 1)
            c = x[0].split(':')[0]
            v = x[0].split(':')[1]
            b = x[1].split('->')[0].strip()
            a = x[1].split('->')[1].strip()
            if a == '~': a = ''
            
            if not ((book + u' ' + c + u':' + v) in self.versesPatched):
                patchesAlreadyApplied.append(book + u' ' + c + u':' + v)
                self.versesPatched.append(book + u' ' + c + u':' + v)
            elif not ((book + u' ' + c + u':' + v) in patchesAlreadyApplied):
                self.debugPrint('      WARNING: already patched ' + (book + u' ' + c + u':' + v))
            else:
                # We have changed this verse, but it was in this patch so
                # we assume the patcher knows what they are doing
                pass
    
            r = self.rangeOfChapter(s,c,0,len(s))
            r = self.rangeOfVerse(s,v,r[0],r[1])
            ii = r[0]
            i2 = self.findPatch(s, b.replace('~', '\n'), r[0], r[1])
            if i2 == -1:
                self.debugPrint('ERROR finding BEFORE at ' + lines[i])
                self.debugPrint(str(r[0]) + ' ... ' + str(r[1]))
                self.debugPrint(s[r[0]:r[1]])
                self.debugPrint(str(ii))
                sys.exit()
            else:
                s = s[0:i2] + a.replace('~', '\n') + s[i2+len(b):len(s)]
                i = i + 1
        return s
         
    def debugPrint(self, st):
        # Change this for noisier reporting
        if st[:5] == 'ERROR':
            print '              ' + st.encode('utf-8')
        
    def rangeOfChapter(self, s, c, start, finish):
        return self.rangeOfEntity('CHAPTER', u'\\c ', s, c, start, finish)

    def rangeOfVerse(self, s, v, start, finish):
        return self.rangeOfEntity('VERSE', u'\\v ', s, v, start, finish)

    def rangeOfEntity(self, name, entity, s, v, start, finish):
        i = s.find((entity + v), start, finish)
        if i == -1:
            self.debugPrint('ERROR finding start of ' + name + ' at ' + v)
            self.debugPrint(s[start:finish])
            sys.exit()
        i2 = s.find(entity, i + 1, finish)
        if i2 == -1:
            i2 = finish
        return (i, i2)

    def isSeparator(self, c):
        s = u"""\n\t -.,!? —‘“”’;:()'"\\"""
        return s.find(c) != -1
        
        
