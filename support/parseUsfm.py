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
    return usfm.parseString( aString )
