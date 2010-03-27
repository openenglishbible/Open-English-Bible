import re
import os
import parseUsfm


class TexPrinter(object):
    def renderID(self, token):      return ""
    def renderIDE(self, token):     return ""
    def renderH(self, token):       return '\RAHeader{' + token.value + '} '
    def renderMT(self, token):      return '\MT{' + token.value + '} '
    def renderMS(self, token):      return '\MS{' + token.value + '} '
    def renderMS2(self, token):     return '\MSS{' + token.value + '} '
    def renderP(self, token):       return '\indenting[yes]\par '
    def renderS(self, token):       return '\\blank\indenting[no]\par'
    def renderC(self, token):
        if not token.value == '1':
            return '\n \C{' + token.value + '} '
        else:
            return ''
    def renderV(self, token):
        if not (token.value == '1' or token.value == ''):
            return '\n \V{' + token.value + '} '
        else:
            return ''
    def renderWJS(self, token):     return ""
    def renderWJE(self, token):     return ""
    def renderTEXT(self, token):    return " " + token.value + " "
    def renderQ(self, token):       return ""
    def renderQ1(self, token):      return ""
    def renderQ2(self, token):      return ""
    def renderNB(self, token):      return ""


class TransformToContext(object):

    def markShortVerses(self, tokens):
        # This is manual until I work out how to do it automatically
        d = (
            ('MRK', '3', '24'),
            ('MRK', '4', '3'),
            ('MRK', '9', '40'),
            ('MRK', '10', '5'),
            ('MRK', '10', '18'),
            ('MRK', '14', '17'),
            ('MRK', '14', '39'),
            ('MRK', '15', '25'),
            ('MRK', '15', '30')
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
                                        nextV.value = v.value + ', ' + nextV.value
                                        v.value = ''
                                        return
                                    i = i + 1
                            i = i + 1
                        return
                    i = i + 1
                return
            i = i + 1
        return
            
    def smallCapSections(self, tokens):
        # Deal with sections
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.isS():
                while i < len(tokens):
                    t = tokens[i]
                    if t.isTEXT():
                        t.value = self.smallCapText(t.value)
                        break
                    i = i + 1
            i = i + 1

        return tokens

    def smallCapText(self, s):
        i = 0
        while i < len(s):
            if i < 50:  #we are early, look for comma
                if s[i] == ',' or s[i] == ';' or s[i:i+3] == 'and':
                    s = '\CapStretch{\sc ' + s[:i] + '}' + s[i:]
                    return s
                i = i + 1
            else: # look for space
                if s[i] == ' ':
                    s = '\CapStretch{\sc ' + s[:i] + '}' + s[i:]
                    return s
                i = i + 1
        return'\CapStretch{\sc ' + s + '}'


    def lineDropFirstChapter(self, tokens):
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t.isC():
                if t.value == '1':
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
                    s = '\lettrine[Lines=3, Ante={\C{1}}]{' + s[0] + '}{\CapStretch{\sc ' + s[1:i] + '}}' + s[i:]
                    return s
                i = i + 1
            else: # look for space
                if s[i] == ' ':
                    s = '\lettrine[Lines=3, Ante={\C{1}}]{' + s[0] + '}{\CapStretch{\sc ' + s[1:i] + '}}' + s[i:]
                    return s
                i = i + 1
        # return lot
        return '\lettrine[Lines=3, Ante={\C{1}}]{' + s[0] + '}{\CapStretch{\sc ' + s[1:] + '}}'


    def translateBook(self, name):

        f = open(self.patchedDir + '/' + name + '.usfm')
        fc = f.read()
        f.close()

        tokens = parseUsfm.parseString(fc)
        self.markShortVerses(tokens)
        tokens = self.smallCapSections(tokens)
        #tokens = self.lineDropFirstChapter(tokens)

        s = ''
        for t in tokens: s = s + t.renderOn(TexPrinter())
        s = s + "\marking[RAChapter]{ } \marking[RABook]{ } \marking[RASection]{ }"

        return s

    def saveAll(self, allBooks):

        s = r"""

        \definemarking[RAChapter]
        \definemarking[RABook]
        \definemarking[RASection]

        \setuppapersize [A5][letter]
    %	\setuparranging [2UP,rotated,doublesided]
        \setuppagenumbering [alternative=doublesided]
        \setuplayout [location=middle, marking=on]

    %	\definefontsynonym [HoeflerTextRegular] [file:HoeflerText-Regular] [features=default]
    %	\definefontsynonym [HoeflerTextItalic] [file:HoeflerText-Italic] [features=default]
    %	\definefontsynonym [HoeflerTextBold] [file:HoeflerText-Black] [features=default]
    %	\definefontsynonym [Serif] [HoeflerTextRegular]
    %	\definefontsynonym [SerifBold] [HoeflerTextBold]
    %	\definefontsynonym [SerifItalic] [HoeflerTextItalic]

        \usetypescript[pagella][handling][highquality]
    %	\definefontfeature [hz] [default] [protrusion=pure, mode=node, script=latn]
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
        \setupindenting[yes, small, next]
        \setupinterlinespace[line=13pt] % Line spacing

        \define[1]\V{\setupinmargin[style=small] \inmargin{#1}}
        \define[1]\C{\setupinmargin[style=bold] \inmargin{#1} \marking[RAChapter]{#1}}
        \define[1]\MS{\section{#1} \marking[RASection]{#1}}
        \define[1]\MSS{{\midaligned{\em #1}}}
        \define[1]\MT{{\midaligned{\sc #1}}\blank ~}
        \define[1]\RAHeader{\chapter{#1} \marking[RABook]{#1}}

        \emergencystretch\maxdimen

        \setuphead[chapter][number=no, textstyle=cap, before=\blank, after=\blank, align={middle, nothyphenated, verytolerant}]
        \setuphead[section][number=no, textstyle=em, before=\blank, after=\blank, align={middle, nothyphenated, verytolerant}]

        \setuplist[chapter][alternative=c]

        \def\CapStretchAmount{.08em}
        \def\CapStretch#1{\def\stretchedspaceamount{\CapStretchAmount}\stretchednormalcase{#1}}

        \usemodule[lettrine]

        \starttext

        \title{Open English Bible}

        \title{Table of Contents}
        \placelist[chapter]
        """ + allBooks + r"""

        \stoptext

        """

        f = open(self.outputDir + '/Bible.tex', 'w')
        f.write(s.encode('utf-8'))
        f.close()

    def setupAndRun(self, patchedDir, prefaceDir, outputDir):
        self.patchedDir = patchedDir
        self.prefaceDir = prefaceDir
        self.outputDir = outputDir

        # Setup list of patches and books to use
        #
        books = os.listdir(self.patchedDir)
        books = [b[:-5] for b in books if b[-5:] == '.usfm']
        preface = unicode(open(self.prefaceDir + '/preface.tex').read(), 'utf-8').strip()
        bookTex = preface
        for book in books:
            bookTex = bookTex + unicode(self.translateBook(book), 'utf-8')
        self.saveAll(bookTex)