import re
import os
import parseUsfm


class TexPrinter(object):
    def __init__(self):
        self.printerState = {u'li': False, u'narrower': False, u'd': False}
        self.smallCapSections = True  # Sometimes we don't want to do this, like for Psalms
        self.justDidLORD = False
        self.justDidNB = False

    def startNarrower(self, n):
        s = u''
        if u'narrower' in self.printerState and self.printerState[u'narrower'] == True:
            self.printerState[u'narrower'] = False
            s = s + u'}'
        else:
            s = s + u'\n\\blank[medium]'
        self.printerState[u'narrower'] = True
        s = s + u'\n\Q{' + str(n) + u'}{'
        self.justDidNB = True
        return s

    def stopNarrower(self):
        s = u''
        if u'narrower' in self.printerState and self.printerState[u'narrower'] == True:
            self.printerState[u'narrower'] = False
            s = s + u'}\\blank[medium]'
        return s

    def escapeText(self, s):
        return s.replace('&', '\\&').replace('%', '\\%')
 
    def markForSmallCaps(self):
        self.printerState[u'smallcaps'] = True

    def renderSmallCaps(self, s):
        if u'smallcaps' in self.printerState and self.printerState[u'smallcaps'] == True:
            self.printerState[u'smallcaps'] = False
            return self.smallCapText(s)
        return s

    def smallCapText(self, s):
         if not self.smallCapSections: 
             # So we don't muck up Psalms
             return s
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
                    
    def renderID(self, token):      return u''
    def renderIDE(self, token):     return u''
    def renderH(self, token):       return u'\RAHeader{' + token.value + u'} '
    def renderMT(self, token):      return self.stopLI() + self.stopNarrower() + u'\MT{' + token.value + u'} '
    def renderMS(self, token):      self.justDidNB = True; self.markForSmallCaps() ; return self.stopNarrower() + u'\MS{' + token.value + u'}'
    def renderMS2(self, token):     self.justDidNB = True; self.markForSmallCaps() ; return self.stopNarrower() + u'\MSS{' + token.value + '}'
    def renderP(self, token):
        s = self.stopD() + self.stopLI() + self.stopNarrower() + u'\n\n'
        if self.justDidNB:
            self.justDidNB = False
            s = s + '\indentation '
        return s 
    def renderB(self, token):       return self.stopD() + self.stopLI() + self.stopNarrower() + u'\\blank\n\n'
    def renderS(self, token):       self.justDidNB = True; return self.stopD() + self.stopLI() + self.stopNarrower() + u'\\blank\n\n\\noindentation '
    def renderC(self, token):
        if not token.value == u'1':
            return u'\C{' + token.value + u'} '
        else:
            return u''
    def renderV(self, token):
        if not (token.value == u'1' or token.value == u''):
            return u'\V{' + token.value + u'} '
        else:
            return ''
    def renderWJS(self, token):     return u""
    def renderWJE(self, token):     return u""
    def renderTEXT(self, token):
        s = self.escapeText(token.value)
        if self.justDidLORD:
            if s[0].isalpha():
                s = u' ' + s
                self.justDidLORD = False
        return self.renderSmallCaps(s)
    def renderQ(self, token):       return self.stopD() + self.stopLI() + self.startNarrower(1)
    def renderQ1(self, token):      return self.stopD() + self.stopLI() + self.startNarrower(1)
    def renderQ2(self, token):      return self.stopD() + self.stopLI() + self.startNarrower(2)
    def renderQ3(self, token):      return self.stopD() + self.stopLI() + self.startNarrower(3)
    def renderNB(self, token):
        self.justDidNB = True
        return self.stopD() + self.stopLI() + self.stopNarrower() + u"\n\n\\noindentation "
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
    
class TransformToContext(object):

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
        tp = TexPrinter()
        tp.smallCapSections = smallCap
        for t in tokens: s = s + t.renderOn(tp)
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

        \define[1]\V{\setupinmargin[style=small] \inmargin{#1}}
        \define[1]\C{\setupinmargin[style=bold] \inmargin{#1} \marking[RAChapter]{#1}}
        \define[1]\MS{\section{#1} \marking[RASection]{#1}\blank\par \noindentation }
        \define[1]\MSS{{\midaligned{\em #1}}\blank\par \noindentation }
        \define[1]\MT{{\midaligned{\sc #1}}\blank ~}
        \define[1]\RAHeader{\chapter{#1} \marking[RABook]{#1}}
        \define[2]\Q{\startnarrower[#1*left,1*right]\noindentation #2\stopnarrower }

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
                    'Revelation',
                    'Psalms']
                 
        fn = self.prefaceDir + '/preface.tex'
        if not os.path.isfile(fn):
            print(fn + ' Not Found')
            preface = u''
        else:
            preface = unicode(open(fn).read(), 'utf-8').strip()
        bookTex = preface
        for book in books:
            bookTex = bookTex + self.translateBook(book, smallCap)
            print '      (' + book + ')'
        self.saveAll(bookTex)