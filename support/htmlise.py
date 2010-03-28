import os
import parseUsfm

class HTMLPrinter(object):
    def __init__(self):
        pass

    def renderID(self, token):      return ""
    def renderIDE(self, token):     return ""
    def renderH(self, token):       return '<h1>' + token.value + '</h1>'
    def renderMT(self, token):      return '<h2>' + token.value + '</h2>'
    def renderMS(self, token):      return '<h3>' + token.value + '</h3>'
    def renderMS2(self, token):     return '<h4>' + token.value + '</h4>'
    def renderP(self, token):       return '<p />'
    def renderS(self, token):       return '<p /><p />'
    def renderC(self, token):       return '<chapter>' + token.value + '</chapter>'
    def renderV(self, token):       return '<verse>' + token.value + '</verse>'
    def renderWJS(self, token):     return ""
    def renderWJE(self, token):     return ""
    def renderTEXT(self, token):    return " " + token.value + " "
    def renderQ(self, token):       return ''
    def renderQ1(self, token):      return ''
    def renderQ2(self, token):      return ''
    def renderNB(self, token):      return ''

class TransformToHTML(object):

    def translateBook(self, name):

        f = open(self.patchedDir + '/' + name + '.usfm')
        fc = f.read()
        f.close()

        tokens = parseUsfm.parseString(fc)

        s = ''
        tp = HTMLPrinter()
        for t in tokens: s = s + t.renderOn(tp)
        return s

    def saveAll(self, allBooks):

        s = """
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
        books = os.listdir(self.patchedDir)
        books = [b[:-5] for b in books if b[-5:] == '.usfm']
        #preface = unicode(open(self.prefaceDir + '/preface.tex').read(), 'utf-8').strip()
        #bookTex = preface
        bookTex = ''
        for book in books:
            bookTex = bookTex + unicode(self.translateBook(book), 'utf-8')
        self.saveAll(bookTex)