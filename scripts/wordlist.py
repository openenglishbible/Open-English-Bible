# -*- coding: utf-8 -*-
 
f = open('../built/Bible.txt')
fc = unicode(f.read(), 'utf-8')
f.close()
 
# create a list of words separated at whitespaces
wordList = fc.split()

clean = []
for w in wordList:
    nw = u''
    for c in w:
        if not c in u"""\n\t .,!? —‘“”’;:()'"[]\\0123456789&*/=""":
            nw = nw + c
    clean.append(nw)
    #clean.append(nw.lower())


noDupes=[]
[noDupes.append(i) for i in clean if not noDupes.count(i)]

filtered=[]
[filtered.append(i) for i in noDupes if i[-3:] == u'eth' or i[-3:] == u'est']

result = u''
for n in filtered: result = result + u'\n' + n

f = open('wordlist', 'w')
f.write(result)
f.close()
