# -*- coding: utf-8 -*-
#

import sys, getopt

from pyparsing import CharsNotIn, ZeroOrMore, Group, Suppress, OneOrMore, ParseResults, Optional, StringEnd

phrase = CharsNotIn( u"[|]"  )
tag = CharsNotIn( u"[|]:,"  )
tags = Group( Optional(tag, default="base") + ZeroOrMore( Suppress(',') + tag ) + Suppress(":") )
option = Group( tags + Optional(phrase, default='') )
optionList = Group( Suppress("[") + option + ZeroOrMore( Suppress('|') + option )  + Suppress("]") ) 
text = OneOrMore( phrase | optionList ) + Suppress( StringEnd() )

# input string
def clean( unicodeString ):
    # We need to clean the input a bit. For a start, until
    # we work out what to do, non breaking spaces will be ignored
    # ie 0xa0
    return unicodeString.replace(u'\xa0', u' ')

def parseString( unicodeString ):
    try:
        s = clean(unicodeString)
        tokens = text.parseString(s, parseAll=True )
    except Exception as e:
        print e
        print repr(unicodeString[:50])
        sys.exit()
    return tokens
    
def render( unicodeString, tags):
    s = parseString( unicodeString )
    r = u''
    for e in s:
        if type(e) == type(u'') or type(e) == type(''):
            r = r + e
        elif type(e) == ParseResults:
            for o in e:
                 if len(set(tags).intersection(o[0])) > 0:
                    r = r + o[1]
        else:
            print type(e)
            print 'WTF?'
            sys.exit()
    return r
    
def listChanges( unicodeString, tags):
    chapter = u'-'
    verse = u'-'
    s = parseString( unicodeString )
    r = u''
    for e in s:
        if type(e) == type(u'') or type(e) == type(''):
            if ur'\v ' in e:
                verse = e[e.rfind(ur'\v ') +3:e.rfind(ur'\v ') + 10].split()[0]
            if ur'\c ' in e:
                chapter = e[e.rfind(ur'\c ') +3:e.rfind(ur'\c ') + 10].split()[0]
        elif type(e) == ParseResults:
            for o in e:
                 if len(set(tags).intersection(o[0])) > 0:
                    r = r + u'\n' + chapter + u':' + verse
                    for op in e:
                         r = r + u'\n\t' + unicode(op[0]) + u' -> ' + unicode(op[1])
        else:
            print type(e)
            print 'WTF?'
            sys.exit()
    return r    
                        
def testHello():
    hello = u"This is an option [test,t2:Hello, World!|oed:Goodbye]."
    assert( str(parseString( hello )) == str([u'This is an option ', [[[u'test', u't2'], u'Hello, World!'], [[u'oed'], u'Goodbye']], u'.']) )
 
def testHelloRender():
    hello = u"This is an option [test,t2:Hello, World!|oed:Goodbye]."
    assert( str(render( hello, ['oed'] )) == u'This is an option Goodbye.') 
    assert( str(render( hello, ['test'] )) == u'This is an option Hello, World!.') 
    assert( str(render( hello, ['t2','oed'] )) == u'This is an option Hello, World!Goodbye.') 

def testEmptyRender():
    hello = u"This is an option [test,t2:Hello, World!|oed:]."
    assert( str(render( hello, ['oed'] )) == u'This is an option .') 
    assert( str(render( hello, ['test'] )) == u'This is an option Hello, World!.') 
    assert( str(render( hello, ['t2','oed'] )) == u'This is an option Hello, World!.') 
   
def testEmptyTags():
    hello = u"This is an option [:Hello, World!|oed:something]."
    assert( str(render( hello, ['oed'] )) == u'This is an option something.') 
    assert( str(render( hello, ['base'] )) == u'This is an option Hello, World!.') 
   
def tests():
    testHello()
    testHelloRender()
    testEmptyRender()
    testEmptyTags()
    print "Tests OK"
    
def usage():
    print """
        OEB-Tools
        ----------

        Variant handler. See source for details.
        
        python versions.py -i infile -o outfile -t tag+anothertag
        
    """

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ui:o:t:c", ["unittest","in=", "out=", "tags=",'changes'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    action = 'b'
    for opt, arg in opts:
        if opt in ("-i", "--in"):
            inF =  arg
        elif opt in ("-o", "--out"):
            outF = arg
        elif opt in ("-t", "--tags"):
            tags = arg.split('+')
        elif opt in ("-u", "--unittest"):
            tests()
            sys.exit(0)
        elif opt in ("-c", "--changes"):
            action = 'c'
            
    if action == 'c':
        f = open(inF)
        s = unicode(f.read(), 'utf-8')
        f.close()
        print listChanges(s,tags)
    else:
        f = open(inF)
        s = unicode(f.read(), 'utf-8')
        f.close()
        s = render(s,tags)
        f = open(outF,'w')
        f.write(s.encode('utf-8'))
        f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
