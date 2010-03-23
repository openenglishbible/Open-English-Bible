import os
import commands

# Setup list of patches and books to use
#
patches = os.listdir('patches')
patches = [p[:-6] for p in patches if p[-6:] == '.patch']
books = os.listdir('source')
books = [b[:-5] for b in books if b[-5:] == '.usfm']

# Setup 'patched' folder for use
#
commands.getoutput('rm -r patched')
commands.getoutput('mkdir patched')
commands.getoutput('cp -r source/* patched/' )
#commands.getoutput('cp -r /Users/russellallen/Documents/Development/Context/way/* /Users/russellallen/Documents/Development/Context/new/' )


def debugPrint(st):
	pass

# For each patch, make changes
#
for patch in patches:
	
	debugPrint('Starting ' + patch)

	f = open('patches/' + patch + '.patch')
	p = unicode(f.read(), 'utf-8').strip()
	f.close()

	lines = p.strip().splitlines()
	lines = [line for line in lines if not (line.isspace() or line == '')]  # Remove empty lines
	lines = [line for line in lines if (not line[0] == ';')]  # Remove comments
	
	i = 0
	while i < len(lines):
		book = lines[i].strip()[3:-1]
		debugPrint('    ' + book)
		bookname = 'patched/' + book + '.usfm'
		f = open(bookname)
		s = unicode(f.read(), 'utf-8')
		f.close()

		i = i + 1
		while i < len(lines) and (not (lines[i].strip()[:3] == 'In ')):
			x = lines[i].strip().split(None, 1)
			c = x[0].split(':')[0]
			v = x[0].split(':')[1]
			b = x[1].split('->')[0].strip()
			a = x[1].split('->')[1].strip()
			
			i2 = s.find(u'\\c ' + c, 0)
			if i2 == -1:
				debugPrint('ERROR finding CHAPTER at ' + lines[i]) 
				
			i2 = s.find((u'\\v ' + v), i2)
			if i2 == -1:
				debugPrint('ERROR finding VERSE at ' + lines[i]) 
				
			i2 = s.find(b, i2)
			if i2 == -1:
				debugPrint('ERROR finding BEFORE at ' + lines[i]) 
				
			debugPrint('      > ' + s[i2:i2 + len(b)])
				
			s = s[0:i2] + a + s[i2+len(b):len(s)]

			debugPrint('        ' + s[i2:i2 + len(a)])

			i = i + 1
			
		f = open(bookname, 'w')
		f.write(s.encode('utf-8'))
		f.close()

		
