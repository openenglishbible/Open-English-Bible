import sys
sys.path.append("support")

import commands

import patch
import texise

# Create patched usfm
print 'Patching...'
p = patch.Patcher()
p.setup('source', 'patches', 'patched')
p.patch()

# Convert to ConTeXt
print 'Converting to TeX...'
c = texise.TransformToContext()
c.setupAndRun('patched', 'preface', 'working/tex')

# Build PDF
print 'Building PDF..'
#print commands.getoutput(""". ../../context/tex/setuptex ; cd working/tex-working; rm * ; context ../tex/Bible.tex; cp *.pdf ../../built/""")
print 'Finished.'