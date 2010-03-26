# -*- coding: utf-8 -*-
#

from pyparsing import Word, alphas, OneOrMore, nums, Literal, White, Group, Suppress, Empty, NoMatch, Optional, CharsNotIn

def usfmToken(key): return Group(Suppress(backslash) + Literal( key ) + Suppress(White()))
def usfmTokenValue(key, value): return Group(Suppress(backslash) + Literal( key ) + Suppress(White()) + value )
def usfmTokenNumber(key): return Group(Suppress(backslash) + Literal( key ) + Suppress(White()) + Word (nums) + Suppress(White()))


# define grammar
phrase      = Word( alphas + "-.,!? —‘“”’;:()" + nums )
backslash   = Literal("\\")

id      = usfmTokenValue( "id", phrase )
ide     = usfmTokenValue( "ide", phrase )
h       = usfmTokenValue( "h", phrase )
mt      = usfmTokenValue( "mt", phrase )
ms      = usfmTokenValue( "ms", phrase )
ms2     = usfmTokenValue( "ms2", phrase )
s       = usfmToken("s")
p       = usfmToken("p")
c       = usfmTokenNumber("c")
v       = usfmTokenNumber("v")
wjs     = usfmToken("wj")
wje     = usfmToken("wj*")
textBlock   = Group(Optional(NoMatch(), "text") + phrase )

element = ide | id | h | mt | ms | ms2 | s | p | c | v | wjs | wje | textBlock
usfm    = OneOrMore( element )

# input string
def parseString( aString ):
    tokens = usfm.parseString( aString )
    return [createToken(t) for t in tokens]

def createToken(t):
    options = {
        'id':   IDToken,
        'ide':  IDEToken,
        'h':    HToken,
        'mt':   MTToken,
        'ms':   MSToken,
        'ms2':  MS2Token,
        'p':    PToken,
        's':    SToken,
        'c':    CToken,
        'v':    VToken,
        'wj':   WJSToken,
        'wj*':  WJEToken,
        'text': TEXTToken
    }
    for k, v in options.iteritems():
        if t[0] == k:
            if len(t) == 1:
                return v()
            else:
                return v(t[1])
    raise Exception(t[0])

class UsfmToken(object):
    def __init__(self, value=None):
        self.value = value
    def isID(self):     return False
    def isIDE(self):    return False
    def isH(self):      return False
    def isMT(self):     return False
    def isMS(self):     return False
    def isMS2(self):    return False
    def isP(self):      return False
    def isS(self):      return False
    def isC(self):      return False
    def isV(self):      return False
    def isWJS(self):    return False
    def isWJE(self):    return False
    def isTEXT(self):   return False

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
