import re
import os
import parseUsfm
import books

class TexPrinter(object):
    def __init__(self):
        self.printerState = {u'li': False, u'd': False}
        self.smallCapSections = True  # Sometimes we don't want to do this, like for Psalms
        self.justDidLORD = False
        self.justDidNB = False
        self.doNB = False
        self.narrower = False
        self.doChapterOrVerse = u''
        self.smallcaps = False

    def startNarrower(self, n):
        s = u'}' if self.narrower else u'\n\\blank[medium] '
        self.narrower = True
        s = s + u'\n\\noindentation \\Q{' + str(n) + u'}{'
        self.doNB = True
        return s

    def stopNarrower(self):
        s = u'}\n\\blank[medium] ' if self.narrower else u''
        self.narrower = False
        return s

    def escapeText(self, s):
        return s.replace('&', '\\&').replace('%', '\\%')
 
    def markForSmallCaps(self):
        if self.smallCapSections: 
             self.smallcaps = True

    def renderSmallCaps(self, s):
        if self.smallcaps == True:
            self.smallcaps = False
            return self.smallCapText(s)
        return s

    def smallCapText(self, s):
         i = 0
         while i < len(s):
             if i < 30:  #we are early, look for comma
                 if s[i] == u',' or s[i] == u';' or s[i:i+3] == u'and':
                     s = u'\CapStretch{' + s[:i] + u'}' + s[i:]
                     return s
                 i = i + 1
             else: # look for space
                 if s[i] == ' ':
                     s = u'\CapStretch{' + s[:i] + u'}' + s[i:]
                     return s
                 i = i + 1
         return u'\CapStretch{' + s + u'}'
         
    def startLI(self):
        if self.printerState[u'li'] == False:
            self.printerState[u'li'] = True
            return u'\startitemize \item '
        else:
            return u'\item '
        
    def stopLI(self):
        if self.printerState[u'li'] == False:
            return u''
        else:
            self.printerState[u'li'] = False
            return u'\stopitemize'

    def startD(self):
        if self.printerState[u'd'] == False:
            self.printerState[u'd'] = True
        return u'\par {\startalignment[center] \em '

    def stopD(self):
        if self.printerState[u'd'] == False:
            return u''
        else:
            self.printerState[u'd'] = False
            return u'\stopalignment }'
            
    def newLine(self):
        s = u'\n\par \n'
        if self.doNB:
            self.doNB = False
            self.justDidNB = True
            s = s + u'\\noindentation '
        elif self.justDidNB:
            self.justDidNB = False
            s = s + u'\indentation '
        return s
                    
    def renderID(self, token):      return u''
    def renderIDE(self, token):     return u''
    def renderH(self, token):       return u'\n\n\RAHeader{' + token.value + u'}\n'
    def renderMT(self, token):      return self.stopLI() + self.stopNarrower() + u'\n\MT{' + token.value + u'}\n'
    def renderMS(self, token):      self.doNB = True; self.markForSmallCaps() ; return self.stopNarrower() + u'\n\MS{' + token.value + u'}' + self.newLine()
    def renderMS2(self, token):     self.doNB = True; self.markForSmallCaps() ; return self.stopNarrower() + u'\n\MSS{' + token.value + '}' + self.newLine()
    def renderP(self, token):       return self.stopD() + self.stopLI() + self.stopNarrower() + self.newLine() 
    def renderB(self, token):       return self.stopD() + self.stopLI() + self.stopNarrower() + u'\\blank \n'
    def renderS(self, token):       self.doNB = True; return self.stopD() + self.stopLI() + self.stopNarrower() +  u'\n\\blank[big] ' + u'\n\MSS{' + token.value + '}' + self.newLine() 
    def renderS2(self, token):      self.doNB = True; return self.stopD() + self.stopLI() + self.stopNarrower() + u'\n\\blank[big] ' + u'\n\MSS{' + token.value + '}' + self.newLine() 
    def renderC(self, token):
        if not token.value == u'1':
            self.doChapterOrVerse = u'\C{' + token.value + u'}'
        return u' '
    def renderV(self, token):
        if not token.value == u'1':
            self.doChapterOrVerse =  u'\V{' + token.value + u'}'
        return ' '
    def renderWJS(self, token):     return u""
    def renderWJE(self, token):     return u""
    def renderTEXT(self, token):
        s = self.escapeText(token.value)
        if self.smallcaps and not self.doChapterOrVerse == u'':
            s = self.renderSmallCaps(s)
            i = s.find(u'}')
            s = s[0:i+1] + self.doChapterOrVerse + s[i+1:]
            self.doChapterOrVerse = u''
        elif not self.doChapterOrVerse == u'':
            i = s.find(u' ')              
            s = s[0:i] + self.doChapterOrVerse + s[i+1:]
            self.doChapterOrVerse = u''
        elif self.smallcaps:
            s = self.renderSmallCaps(s)
        if self.justDidLORD:
            if s[0].isalpha():
                s = u' ' + s
            self.justDidLORD = False    
        return s
    def renderQ(self, token):       return self.stopD() + self.stopLI() + self.startNarrower(1)
    def renderQ1(self, token):      return self.stopD() + self.stopLI() + self.startNarrower(1)
    def renderQ2(self, token):      return self.stopD() + self.stopLI() + self.startNarrower(2)
    def renderQ3(self, token):      return self.stopD() + self.stopLI() + self.startNarrower(3)
    def renderNB(self, token):      self.doNB = True ; return self.stopD() + self.stopLI() + self.stopNarrower() + u'\\blank[medium] ' + self.newLine() 
    def renderQTS(self, token):     return u''
    def renderQTE(self, token):     return u''
    def renderFS(self, token):      return u'\\footnote{'
    def renderFE(self, token):      return u'}'
    def renderIS(self, token):      return u'{\em '
    def renderIE(self, token):      return u'}'
    def renderADDS(self, token):    return u'{\em '
    def renderADDE(self, token):    return u'}'
    def renderNDS(self, token):     return u'{\sc '
    def renderNDE(self, token):     self.justDidLORD = True; return u'}'
    def renderLI(self, token):      return self.startLI()
    def renderD(self, token):       return self.startD()
    def renderSP(self, token):      return self.startD()
    def renderPBR(self, token):     return u' \\\\ '
    
class TransformToContext(object):
    
    texPrinter = None

    def markShortVerses(self, tokens):
        # This is manual until I work out how to do it automatically
        d = (
            (u'MRK', u'3',  u'24'),
            (u'MRK', u'4',  u'3'),
            (u'MRK', u'9',  u'40'),
            (u'MRK', u'10', u'5'),
            (u'MRK', u'10', u'18'),
            (u'MRK', u'14', u'17'),
            (u'MRK', u'14', u'39'),
            (u'MRK', u'15', u'25'),
            (u'MRK', u'15', u'30')
        )
        for t in d:
            self.findAndMarkVerse(tokens, t[0], t[1], t[2])

    def findAndMarkVerse(self, tokens, book, chapter, verse):
        i = 0
        while i < len(tokens):
            b = tokens[i]
            if b.isID() and (b.value == book):
                while i < len(tokens):
                    c = tokens[i]
                    if c.isC() and (c.value == chapter):
                        while i < len(tokens):
                            v = tokens[i]
                            if v.isV() and verse == v.value:
                                i = i + 1
                                while i < len(tokens):
                                    nextV = tokens[i]
                                    if nextV.isV():
                                        nextV.value = v.value + u', ' + nextV.value
                                        v.value = ''
                                        return
                                    i = i + 1
                            i = i + 1
                        return
                    i = i + 1
                return
            i = i + 1
        return
            
    def lineDropFirstChapter(self, tokens):
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.isC():
                if t.value == u'1':
                    while i < len(tokens):
                        t = tokens[i]
                        if t.isTEXT():
                            t.value = self.lineDropFirstChapterText(t.value)
                            break
                        i = i + 1
            i = i + 1

        return tokens

    def lineDropFirstChapterText(self, s):
        print s
        i = 0
        while i < len(s):
            if i < 50:  #we are early, look for comma
                if s[i] == ',' or s[i] == ';' or s[i:i+3] == 'and':
                    s = u'\lettrine[Lines=3, Ante={\C{1}}]{' + s[0] + u'}{\CapStretch{\sc ' + s[1:i] + u'}}' + s[i:]
                    return s
                i = i + 1
            else: # look for space
                if s[i] == ' ':
                    s = u'\lettrine[Lines=3, Ante={\C{1}}]{' + s[0] + u'}{\CapStretch{\sc ' + s[1:i] + u'}}' + s[i:]
                    return s
                i = i + 1
        # return lot
        return u'\lettrine[Lines=3, Ante={\C{1}}]{' + s[0] + u'}{\CapStretch{\sc ' + s[1:] + u'}}'


    def translateBook(self, name, smallCap):
        
        fn = self.patchedDir + '/' + name + '.usfm'
        if not os.path.isfile(fn):
            print(fn + ' Not Found')
            return u''

        f = open(fn)
        fc = self.stripUnicodeHeader(unicode(f.read(), 'utf-8'))
        f.close()

        tokens = parseUsfm.parseString(fc)
        
        #self.markShortVerses(tokens)
        #tokens = self.lineDropFirstChapter(tokens)

        s = u''
        self.texPrinter.smallCapSections = smallCap
        for t in tokens: s = s + t.renderOn(self.texPrinter)
        s = s + self.texPrinter.stopNarrower()
        s = s + u"\marking[RAChapter]{ } \marking[RABook]{ } \marking[RASection]{ }"

        return s
        
    def stripUnicodeHeader(self, unicodeString):
        if unicodeString[0] == u'\ufeff':
            return unicodeString[1:]
        else:
            return unicodeString

    def saveAll(self, allBooks):

        s = unicode(r"""

        \definemarking[RAChapter]
        \definemarking[RABook]
        \definemarking[RASection]

        \definepapersize [Trade][width=6in, height=9in]
        \setuppapersize [Trade][Trade]
    	%\setuparranging [2UP, rotated, doublesided]
        \setuppagenumbering [alternative=doublesided]
        \setuplayout [location=middle, marking=on]

   % 	\definefontsynonym [HoeflerTextRegular] [file:HoeflerText-Regular] [features=default]
   % 	\definefontsynonym [HoeflerTextItalic] [file:HoeflerText-Italic] [features=default]
   % 	\definefontsynonym [HoeflerTextBold] [file:HoeflerText-Black] [features=default]
   % 	\definefontsynonym [Serif] [HoeflerTextRegular]
   % 	\definefontsynonym [SerifBold] [HoeflerTextBold]
   % 	\definefontsynonym [SerifItalic] [HoeflerTextItalic]

        \usetypescript[pagella][handling][highquality]
    	\definefontfeature [hz] [default] [protrusion=pure, mode=node, script=latn]
    %	\definetypeface [biblefont] [rm] [serif] [pagella] [default] [features=hz]
        \setupbodyfont [pagella, 10.5pt]
        \setupalign [handling]

        \setupbodyfontenvironment[default][em=italic]

        \setuppagenumbering[location=]
        \setupheadertexts[{\em \getmarking[RASection]}][{\getmarking[RABook] ~\getmarking[RAChapter]}]
        \setupfootertexts[pagenumber]
        \setuphead[title][header=high,footer=chapter,page=right]

        \setupspacing[packed]   % normal word space at the end of sentences
        \setupwhitespace[none]  % no space between paragraphs
        \setupindenting[small, yes]
        \setupinterlinespace[line=13pt] % Line spacing

        \define[1]\V{\setupinmargin[style=small] \inmargin{#1} ~}
        \define[1]\C{\setupinmargin[style=bold] \inmargin{#1} \marking[RAChapter]{#1} ~}
        \define[1]\MS{\section{#1} \marking[RASection]{#1}}
        \define[1]\MSS{{\midaligned{\em #1}}}
        \define[1]\MT{{\midaligned{\sc #1}}\blank ~}
        \define[1]\RAHeader{\chapter{#1} \marking[RABook]{#1} }
        \define[2]\Q{\startnarrower[#1*left,1*right] #2\stopnarrower }

        \emergencystretch\maxdimen

        \setuphead[chapter][number=no, textstyle=cap, before=\blank, after=\blank, align={middle, nothyphenated, verytolerant}]
        \setuphead[section][number=no, textstyle=em, before=\blank, after=\blank, align={middle, nothyphenated, verytolerant}]

        \setuplist[chapter][alternative=c]

        \def\CapStretchAmount{.08em}
        \def\CapStretch#1{\def\stretchedspaceamount{\CapStretchAmount}\stretchednormalcase{\sc #1}}

        \usemodule[lettrine]

        \setupnote[footnote][way=bypage]
        
        \starttext

        \title{Open English Bible}

        \title{Table of Contents}
        \placelist[chapter]
        """, 'ascii') + allBooks + ur"""

        \stoptext

        """

        f = open(self.outputDir + '/Bible.tex', 'w')
        f.write(s.encode('utf-8'))
        f.close()

    def setupAndRun(self, patchedDir, prefaceDir, outputDir, smallCap = True):
        self.patchedDir = patchedDir
        self.prefaceDir = prefaceDir
        self.outputDir = outputDir
        self.texPrinter = TexPrinter()
                 
        fn = self.prefaceDir + '/preface.tex'
        if not os.path.isfile(fn):
            print(fn + ' Not Found')
            preface = u''
        else:
            preface = unicode(open(fn).read(), 'utf-8').strip()
        bookTex = preface
        for book in books.books:
            bookTex = bookTex + self.translateBook(book, smallCap)
            print '      (' + book + ')'
        self.saveAll(bookTex)