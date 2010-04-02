import os
import commands
import sys

class Patcher(object):

    def setup(self, sourceDir, patchDir, outputDir):
        self.sourceDir = sourceDir
        self.patchDir = patchDir
        self.outputDir = outputDir
        self.patches = os.listdir(self.patchDir)
        self.patches = [p[:-6] for p in self.patches if p[-6:] == '.patch']
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
        
    def applyPatchToBook(self, b, s, patch):
        self.debugPrint('    ' + patch)

        f = open(self.patchDir + '/' + patch + '.patch')
        p = unicode(f.read(), 'utf-8').strip()
        f.close()

        lines = p.strip().splitlines()
        lines = [line for line in lines if not (line.isspace() or line == '')]  # Remove empty lines
        lines = [line for line in lines if (not line[0] == ';')]                # Remove comments
        
        # Forward to appropriate place
        i = 0
        while i < len(lines) and not b == lines[i].strip()[3:-1]: i = i + 1
        i = i + 1
        
        while i < len(lines) and (not (lines[i].strip()[:3] == 'In ')):
			x = lines[i].strip().split(None, 1)
			c = x[0].split(':')[0]
			v = x[0].split(':')[1]
			b = x[1].split('->')[0].strip()
			a = x[1].split('->')[1].strip()
	
			r = self.rangeOfChapter(s,c,0,len(s))
			r = self.rangeOfVerse(s,v,r[0],r[1])
			ii = r[0]
			i2 = s.find(b, r[0], r[1])
			if i2 == -1:
				self.debugPrint('ERROR finding BEFORE at ' + lines[i])
				self.debugPrint('"' + b + '" >> "' + a + '"')
				self.debugPrint(str(r[0]) + ' ... ' + str(r[1]))
				self.debugPrint(s[r[0]:r[1]])
				self.debugPrint(str(ii))
				sys.exit()
			else:
				s = s[0:i2] + a + s[i2+len(b):len(s)]
				i = i + 1
        return s
         
    def debugPrint(self, st):
        print '      ' + st.encode('utf-8')
        
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



        
