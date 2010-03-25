import re
import os
import parseUsfm

class TransformToContext(object):


    def smallcaps(self, s, i):
        i2 = i
        while i2 < len(s):
            if (i2 - i) < 50:  #we are early, look for comma
                if s[i2] == ',' or s[i2] == ';' or s[i2:i2+3] == 'and':
                    s = s[:i] + '\CapStretch{\sc ' + s[i:i2] + '}' + s[i2:]
                    i2 = len(s) # break
                i2 = i2 + 1
            else: # look for space
                if s[i2] == ' ':
                    s = s[:i] + '\CapStretch{\sc ' + s[i:i2] + '}' + s[i2:]
                    i2 = len(s) # break
                i2 = i2 + 1
        return s

    def smallCapSections(self, s):
        # Deal with sections

        i = 0
        while i < len(s):
            if (s[i:i+2] == '\s') and not (s[i:i+3] == '\sc')  :
                l = len(r'\blank\indenting[no]')
                s = s[:i] + r'\blank\indenting[no]' + s[i+2:]
                i = i + l
                # look forward for start of line
                while s[i].isspace() or (s[i] == '\\') or s[i].isdigit() or (s[i-1] == '\\'):
                    i = i + 1
                s = self.smallcaps(s, i)
                i = 0
            i = i  + 1

        return s

    def lineDropFirstChapter(self, s):
        # Deal with first drop cap

        i = 0
        while (i + 5) < len(s):
            print str(len(s)) + '    ' + str(i + 5)
            while ((i + 5) < len(s)) and not (s[i:i + 4] == '\c 1' and s[i+4].isspace()):
                i = i + 1
            if (i + 5) < len(s):
                i2 = i + 4
                while s[i2].isspace():
                    i2 = i2 + 1
                s = s[:i] + '\lettrine[Lines=3, Ante={\C{1}}]{' + s[i2:i2+1] + '}{GG}' + s[i2+1:]
                i = i2 + 1 + 50
            else:
                return s
        return s

    def translateBook(self, name):

        f = open(self.patchedDir + '/' + name + '.usfm')
        #fc = unicode(f.read(), 'utf-8').strip()
        fc = f.read()
        f.close()

        s = ''
        p = parseUsfm.parseString(fc)

        for token in p:
            if token[0] == 'v':
                if not token[1] == '1':
                    s = s + '\n \V{' + token[1] + '} '
            if token[0] == 'c': s = s + ' \n\C{' + token[1] + '} '
            if token[0] == 'wjs' or token[0] == 'wje': pass
            if token[0] == 'p': s = s + '\indenting[yes]\par '
            if token[0] == 'id' or token[0] == 'ide': pass
            if token[0] == 'h': s = s + '\RAHeader{' + token[1] + '} '
            if token[0] == 'mt': s = s + '\MT{' + token[1] + '} '
            if token[0] == 'ms': s = s + '\MS{' + token[1] + '} '
            if token[0] == 'ms2': s = s + '\MSS{' + token[1] + '} '
            if token[0] == 'text':  s = s + token[1]

        #s = self.smallCapSections(s)

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