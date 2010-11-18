# -*- coding: utf-8 -*-
#

import sys

from pyparsing import Word, alphas, OneOrMore, nums, Literal, White, Group, Suppress, Empty, NoMatch, Optional, CharsNotIn

def usfmToken(key):
    return Group(Suppress(backslash) + Literal( key ) + Suppress(White()))
def usfmBackslashToken(key):
    return Group(Literal(key))
def usfmEndToken(key): 
    return Group(Suppress(backslash) + Literal( key +  u"*"))
def usfmTokenValue(key, value): 
    return Group(Suppress(backslash) + Literal( key ) + Suppress(White()) + Optional(value) )
def usfmTokenNumber(key): 
    return Group(Suppress(backslash) + Literal( key ) + Suppress(White()) + Word (nums) + Suppress(White()))


# define grammar
phrase      = Word( alphas + u"-.,!? —–‘“”’;:()'\"[]/&%=" + nums )
backslash   = Literal(u"\\")
plus        = Literal(u"+")

textBlock   = Group(Optional(NoMatch(), u"text") + phrase )

id      = usfmTokenValue( u"id", phrase )
ide     = usfmTokenValue( u"ide", phrase )
h       = usfmTokenValue( u"h", phrase )
mt      = usfmTokenValue( u"mt", phrase )
ms      = usfmTokenValue( u"ms", phrase )
ms1     = usfmTokenValue( u"ms1", phrase )
ms2     = usfmTokenValue( u"ms2", phrase )
s       = usfmTokenValue( u"s", phrase )
s1      = usfmTokenValue( u"s1", phrase )
s2      = usfmTokenValue( u"s2", phrase )
p       = usfmToken(u"p")
b       = usfmToken(u"b")
c       = usfmTokenNumber(u"c")
v       = usfmTokenNumber(u"v")
wjs     = usfmToken(u"wj")
wje     = usfmEndToken(u"wj")
q       = usfmToken(u"q")
q1      = usfmToken(u"q1")
q2      = usfmToken(u"q2")
q3      = usfmToken(u"q3")
qts     = usfmToken(u"qt")
qte     = usfmEndToken(u"qt")
nb      = usfmToken(u"nb")
fs      = usfmTokenValue(u"f", plus)
fe      = usfmEndToken(u"f")
ist     = usfmToken(u"i")
ien     = usfmEndToken(u"i")
li      = usfmToken(u"li")
d       = usfmToken(u"d")
sp      = usfmToken(u"sp")
adds    = usfmToken(u"add")
adde    = usfmEndToken(u"add")
nds     = usfmToken(u"nd")
nde     = usfmEndToken(u"nd")
pbr     = usfmBackslashToken("\\\\")

element = ide | id | h | mt | ms | ms1 | ms2 | s | s1 | s2 | p | b | c | v | wjs | wje | nds | nde | q | q1 | q2 | q3 | qts | qte | nb | fs | fe | ist | ien | li | d | sp | adds | adde | pbr | textBlock
usfm    = OneOrMore( element )

# input string
def parseString( unicodeString ):
    try:
        tokens = usfm.parseString( unicodeString, parseAll=True )
    except Exception as e:
        print e
        print repr(unicodeString[:50])
        sys.exit()
    return [createToken(t) for t in tokens]

def createToken(t):
    options = {
        u'id':   IDToken,
        u'ide':  IDEToken,
        u'h':    HToken,
        u'mt':   MTToken,
        u'ms':   MSToken,
        u'ms1':  MSToken,
        u'ms2':  MS2Token,
        u'p':    PToken,
        u'b':    BToken,
        u's':    SToken,
        u's1':   SToken,
        u's2':   S2Token,
        u'c':    CToken,
        u'v':    VToken,
        u'wj':   WJSToken,
        u'wj*':  WJEToken,
        u'q':    QToken,
        u'q1':   Q1Token,
        u'q2':   Q2Token,
        u'q3':   Q3Token,
        u'nb':   NBToken,
        u'qt':   QTSToken,
        u'qt*':  QTEToken,
        u'f':    FSToken,
        u'f*':   FEToken,
        u'i':    ISToken,
        u'i*':   IEToken,
        u'li':   LIToken,
        u'd':    DToken,
        u'sp':   SPToken,
        u'i*':   IEToken,
        u'li':   LIToken,
        u'add':  ADDSToken,
        u'add*': ADDEToken,
        u'nd':   NDSToken,
        u'nd*':  NDEToken,
        u'\\\\':  PBRToken,
        u'text': TEXTToken
    }
    for k, v in options.iteritems():
        if t[0] == k:
            if len(t) == 1:
                return v()
            else:
                return v(t[1])
    raise Exception(t[0])

class UsfmToken(object):
    def __init__(self, value=u""):
        self.value = value
    def getValue(self): return self.value
    def isID(self):     return False
    def isIDE(self):    return False
    def isH(self):      return False
    def isMT(self):     return False
    def isMS(self):     return False
    def isMS2(self):    return False
    def isP(self):      return False
    def isB(self):      return False
    def isS(self):      return False
    def isS2(self):      return False
    def isC(self):      return False
    def isV(self):      return False
    def isWJS(self):    return False
    def isWJE(self):    return False
    def isTEXT(self):   return False
    def isQ(self):      return False
    def isQ1(self):     return False
    def isQ2(self):     return False
    def isQ3(self):     return False
    def isQTS(self):    return False
    def isQTE(self):    return False
    def isNB(self):     return False
    def isFS(self):     return False
    def isFE(self):     return False
    def isIS(self):     return False
    def isIE(self):     return False
    def isLI(self):     return False
    def isD(self):      return False
    def isSP(self):     return False
    def isADDS(self):   return False
    def isADDE(self):   return False
    def isNDS(self):    return False
    def isNDE(self):    return False
    def isPBR(self):    return False
    
class IDToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderID(self)
    def isID(self):     return True

class IDEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderIDE(self)
    def isIDE(self):    return True

class HToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderH(self)
    def isH(self):      return True

class MTToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMT(self)
    def isMT(self):     return True

class MSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMS(self)
    def isMS(self):     return True

class MS2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMS2(self)
    def isMS2(self):    return True

class PToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderP(self)
    def isP(self):      return True

class BToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderB(self)
    def isB(self):      return True

class CToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderC(self)
    def isC(self):      return True

class VToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderV(self)
    def isV(self):      return True

class TEXTToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTEXT(self)
    def isTEXT(self):   return True

class WJSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderWJS(self)
    def isWJS(self):    return True

class WJEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderWJE(self)
    def isWJE(self):    return True

class SToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderS(self)
    def isS(self):      return True

class S2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderS2(self)
    def isS2(self):      return True

class QToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQ(self)
    def isQ(self):      return True

class Q1Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQ1(self)
    def isQ1(self):      return True

class Q2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQ2(self)
    def isQ2(self):      return True

class Q3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQ3(self)
    def isQ3(self):      return True

class NBToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderNB(self)
    def isNB(self):      return True

class QTSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQTS(self)
    def isQTS(self):      return True

class QTEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQTE(self)
    def isQTE(self):      return True

class FSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFS(self)
    def isFS(self):      return True

class FEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFE(self)
    def isFE(self):      return True

class ISToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderIS(self)
    def isIS(self):      return True

class IEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderIE(self)
    def isIE(self):      return True

class LIToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderLI(self)
    def isLI(self):      return True

class DToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderD(self)
    def isD(self):      return True
    
class SPToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderSP(self)
    def isSP(self):      return True
    
class ADDSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderADDS(self)
    def isADDS(self):    return True

class ADDEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderADDE(self)
    def isADDE(self):    return True

class NDSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderNDS(self)
    def isNDS(self):    return True

class NDEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderNDE(self)
    def isNDE(self):    return True

class PBRToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderPBR(self)
    def isPBR(self):    return True
