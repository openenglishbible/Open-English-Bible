import re
import os

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
        s = unicode(f.read(), 'utf-8').strip()
        f.close()

        # Remove \v 1
        p = re.compile(r'\\v 1(\s)')
        s = p.sub(r'', s)

        s = self.smallCapSections(s)
        #s = lineDropFirstChapter(s)

        # Easier stuff

        p = re.compile(r'\\f')
        s = p.sub(r'', s)

        p = re.compile(r'\\v ([0-9]*)(\s)')
        s = p.sub(r' \\V{\1}', s)

        p = re.compile(r'\\c ([0-9]*)(\s)')
        s = p.sub(r' \\C{\1}', s)

        p = re.compile(r'\\wj(\s)')
        s = p.sub(r' ', s)

        p = re.compile(r'\\wj\*(\s)')
        s = p.sub(r' ', s)

        p = re.compile(r'\\p(\s)')
        s = p.sub(r'\\indenting[yes]\\par\1', s)

        p = re.compile(r'\\id(\s)')
        s = p.sub(r'%\\id\1', s)

        p = re.compile(r'\\ide(\s)')
        s = p.sub(r'%\\ide\1', s)

        p = re.compile(r'\\h (.*)\n')
        s = p.sub(r'\\RAHeader{\1}\n', s)

        p = re.compile(r'\\mt (.*)\n')
        s = p.sub(r'\\MT{\1}\n', s)

        p = re.compile(r'\\ms (.*)\n')
        s = p.sub(r'\\MS{\1}\n', s)

        p = re.compile(r'\\ms2 (.*)\n')
        s = p.sub(r'\\MSS{\1}\n', s)

        # Ignore \q for the moment
        p = re.compile(r'\\q\s')
        s = p.sub(r' ', s)

        # Turn \s into blank line, ignoring smallcaps for the moment
        #p = re.compile(r'\\s(\s)')
        # s= p.sub(r'\\blank\\indenting[no]\1', s)
        # p = re.compile(r'\\s(\s)(.*)\s(.*)\n')
        # s = p.sub(r'\\noindenting\\blank\2 \3\n\indenting[yes]', s)
        #s = p.sub(r'\\SectionPar{\2 \1 \3}', s)

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
            bookTex = bookTex + self.translateBook(book)
        self.saveAll(bookTex)