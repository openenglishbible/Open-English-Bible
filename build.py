import sys
sys.path.append("support")

from subprocess import Popen, PIPE

import patch
import texise
import htmlise

# Create patched usfm
print '#### Patching...'
p = patch.Patcher()
p.setup('source', 'patches', 'patched')
p.patch()

print '#### Building PDF...'

# Convert to ConTeXt
print '     Converting to TeX...'
c = texise.TransformToContext()
c.setupAndRun('patched', 'preface', 'working/tex')

# Build PDF
if True:
    print '     Building PDF..'
    c = """. ../../context/tex/setuptex ; cd working/tex-working; rm * ; context ../tex/Bible.tex; cp *.pdf ../../built/"""
    pp = Popen(c, shell=True, stdout=PIPE)
    for ln in pp.stdout:
        print '     ',ln[:-1]

# Convert to HTML
print '     Converting to HTML...'
c = htmlise.TransformToHTML()
c.setupAndRun('patched', 'preface', 'built')

print '#### Finished.'