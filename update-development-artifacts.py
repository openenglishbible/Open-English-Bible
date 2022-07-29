#!/usr/bin/env python3
import os, os.path
import tempfile
import shutil
import subprocess
import filecmp
import pathlib
import sys
import datetime


##############################
#
#   Functions
#
##############################

def lastModified(book):
    d = 'cd ' + sourceDir + ' ; git log -1 --format="%ad" -- "' + book.sourceFileName() + '"'
    d = subprocess.getoutput(d)
    d = datetime.datetime.strptime(d, '%a %b %d %X %Y %z')
    n = str(d.year) + '.' + str(d.month) + '.' + str(d.day)
    return n

def updateUSFM():
    print('******* UPDATING ' + tags + ' *******')
    print('  Building from: ' + sourceDir)
    print('          using: ' + toolsDir)
    print('           usfm: ' + usfmDir)
    print('            rtf: ' + rtfDir)
    print('            tmp: ' + tempDir)

    run = toolsDir + '/usfm-tools check --oeb -s ' + usfmDir
    subprocess.run(run, shell=True)

    run = toolsDir + '/usfm-tools variant -s ' + sourceDir + ' -d ' + tempDir + ' -t ' + tags + ' -b ' + booklist + ' ' + swap
    subprocess.run(run, shell=True)

    isDifferent = False
    for book in books:
        fm = tempDir  + '/' + book.fileName()
        to = usfmDir + '/' + book.fileName()

        if os.path.isfile(fm) and \
           (not os.path.isfile(to) or not filecmp.cmp(fm, to)):

            # We are different from last run
            isDifferent = True

            # Update USFM
            shutil.move(fm, to)

            # Update RTF
            subprocess.run('rm ' + tempDir2 + '/*', shell=True)
            shutil.copy(to, tempDir2)
            run = toolsDir + '/usfm-tools transform --target=rtf --usfmDir=' + tempDir2 + ' --builtDir=' + rtfDir + ' --config=' + config + ' --name="' + buildId + '-' + book.name() + '"'
            subprocess.run(run, shell=True)

            print('Updated ' + book.fileName())

    # if isDifferent:
    #         # Update Accordance
    #         subprocess.run('rm ' + tempDir2 + '/*', shell=True)
    #         shutil.copy(to, tempDir2)
    #         run = toolsDir + '/usfm-tools transform --target=accordance --usfmDir=' + usfmDir + ' --builtDir=' + indexDir + ' --config=' + config + ' --name="' + buildId + '"'
    #         subprocess.run(run, shell=True)
    #         print('Updated Accordance')

    print('******* UPDATING INDEX *******')
    f = open (indexDir + '/table.html', 'w')
    f.write(table(books))
    f.close()

def templateForBook(b):
    template = """
        <td>
          <span class="{}">{}</span><br>
          <span class="comment"><a href="https://github.com/openenglishbible/Open-English-Bible/blob/master/artifacts/us/rtf/oeb-working-{}.rtf">rtf</a> <a href="https://github.com/openenglishbible/Open-English-Bible/blob/master/source/{}.usfm.db">usfm.db</a><br>{}
          </span>
        </td>
    """
    status = 'absent'
    try:
        f = open(sourceDir + '/' + b.sourceFileName())
        c = f.read()
        f.close()
        if c.find(r'\rem IN RELEASE') > 0: status = 'released'
        elif c.find(r'\rem OK FOR RELEASE') > 0: status = 'checked'
        elif c.find(r'\rem DEVELOPMENT ONLY') > 0: status = 'unchecked'
        else: status = 'unchecked'
        d = lastModified(b)
    except Exception as e:
        status = 'absent'
        d = ''
    return template.format(status, b.full, b.name(), b.name(), d)

def headerLine(s):
    return '<tr class="header"><td colspan="5">' + s + '</td></tr>'

def section(name, books):
    table = headerLine(name)
    if len(books) <= 5:
        table = table + subsection(books)
    elif len(books) <= 10:
        table = table + subsection(books[:5])
        table = table + subsection(books[5:])
    elif len(books) <= 15:
        table = table + subsection(books[:5])
        table = table + subsection(books[5:10])
        table = table + subsection(books[10:])
    elif len(books) <= 20:
        table = table + subsection(books[:5])
        table = table + subsection(books[5:10])
        table = table + subsection(books[10:15])
        table = table + subsection(books[15:20])
    elif len(books) <= 25:
        table = table + subsection(books[:5])
        table = table + subsection(books[5:10])
        table = table + subsection(books[10:15])
        table = table + subsection(books[15:20])
        table = table + subsection(books[20:25])
    return table

def subsection(books):
    table = '<tr>'
    for b in books:
        table = table + templateForBook(b)
    return table + '</tr>'

def table(books):
    table = """<table style="border-spacing: 10px;">"""
    table = table + section('Pentateuch', books[1:6])  # Remember, 'first book' is preface
    table = table + section('Histories', books[6:18])
    table = table + section('Wisdom', books[18:23])
    table = table + section('Major Prophets', books[23:28])
    table = table + section('Minor Prophets', books[28:40])
    table = table + section('Gospels and Acts', books[40:45])
    table = table + section('Letters and Revelation', books[45:67])
    table = table + '</table>'   
    return table

##############################
#
#   Books Data
#
##############################

class Book(object):
  def __init__(self, number, sil, full):
    self.number = number
    self.sil = sil
    self.full = full
    
  def sourceFileName(self):
    return self.name() + '.usfm.db'

  def fileName(self):
    return self.name() + '.usfm'

  def name(self):
    return self.number + '-' + self.full
    
books = []

books.append( Book('00', 'FRT', 'Front Page'      ))
books.append( Book('01', 'GEN', 'Genesis'         ))
books.append( Book('02', 'EXO', 'Exodus'          ))
books.append( Book('03', 'LEV', 'Leviticus'       ))
books.append( Book('04', 'NUM', 'Numbers'         ))
books.append( Book('05', 'DEU', 'Deuteronomy'     ))

books.append( Book('06', 'JOS', 'Joshua'          ))
books.append( Book('07', 'JUD', 'Judges'          ))
books.append( Book('08', 'RUT', 'Ruth'            ))

books.append( Book('09', '1SA', '1 Samuel'        ))
books.append( Book('10', '2SA', '2 Samuel'        ))
books.append( Book('11', '1KI', '1 Kings'         ))
books.append( Book('12', '2KI', '2 Kings'         ))
books.append( Book('13', '1CH', '1 Chronicles'    ))
books.append( Book('14', '2CH', '2 Chronicles'    ))
books.append( Book('15', 'EZR', 'Ezra'            ))
books.append( Book('16', 'NEH', 'Nehemiah'        ))
books.append( Book('17', 'EST', 'Esther'          ))
books.append( Book('18', 'JOB', 'Job'             ))

books.append( Book('19', 'PSA', 'Psalms'          ))
books.append( Book('20', 'PRO', 'Proverbs'        ))
books.append( Book('21', 'ECC', 'Ecclesiastes'    ))
books.append( Book('22', 'SNG', 'Song of Songs'   ))

books.append( Book('23', 'ISA', 'Isaiah'          ))
books.append( Book('24', 'JER', 'Jeremiah'        ))
books.append( Book('25', 'LAM', 'Lamentations'    ))
books.append( Book('26', 'EZK', 'Ezekiel'         ))
books.append( Book('27', 'DAN', 'Daniel'          ))

books.append( Book('28', 'HOS', 'Hosea'           ))
books.append( Book('29', 'JOL', 'Joel'            ))
books.append( Book('30', 'AMO', 'Amos'            ))
books.append( Book('31', 'OBA', 'Obadiah'         ))
books.append( Book('32', 'JON', 'Jonah'           ))
books.append( Book('33', 'MIC', 'Micah'           ))
books.append( Book('34', 'NAM', 'Nahum'           ))
books.append( Book('35', 'HAB', 'Habakkuk'        ))
books.append( Book('36', 'ZEP', 'Zephaniah'       ))
books.append( Book('37', 'HAG', 'Haggai'          ))
books.append( Book('38', 'ZEC', 'Zechariah'       ))
books.append( Book('39', 'MAL', 'Malachi'         ))

books.append( Book('40', 'MAT', 'Matthew'         ))
books.append( Book('41', 'MRK', 'Mark'            ))
books.append( Book('42', 'LUK', 'Luke'            ))
books.append( Book('43', 'JON', 'John'            ))
books.append( Book('44', 'ACT', 'Acts'            ))

books.append( Book('45', 'ROM', 'Romans'))
books.append( Book('46', '1CO', '1 Corinthians'))
books.append( Book('47', '2CO', '2 Corinthians'))
books.append( Book('48', 'GAL', 'Galatians'))
books.append( Book('49', 'EPH', 'Ephesians'))

books.append( Book('50', 'PHP', 'Philippians'))
books.append( Book('51', 'COL', 'Colossians'))
books.append( Book('52', '1TH', '1 Thessalonians'))
books.append( Book('53', '2TH', '2 Thessalonians'))
books.append( Book('54', '1TI', '1 Timothy'))
books.append( Book('55', '2TI', '2 Timothy'))
books.append( Book('56', 'TIT', 'Titus'))
books.append( Book('57', 'PHL', 'Philemon'))
books.append( Book('58', 'HEB', 'Hebrews'))
books.append( Book('59', 'JAS', 'James'))

books.append( Book('60', '1PE', '1 Peter'))
books.append( Book('61', '2PE', '2 Peter'))

books.append( Book('62', '1JN', '1 John'))
books.append( Book('63', '2JN', '2 John'))
books.append( Book('64', '3JN', '3 John'))
books.append( Book('65', 'JUD', 'Jude'))
books.append( Book('66', 'REV', 'Revelation'))

##############################
#
#	Paths
#
##############################

baseDir   = os.path.dirname(os.path.abspath(__file__)) + '/'
toolsDir  = baseDir + 'USFM-Tools'

sourceDir = baseDir + 'source'
tempDir   = tempfile.mkdtemp()
tempDir2  = tempfile.mkdtemp()

for d in [sourceDir, tempDir, tempDir2]:
    pathlib.Path(d).mkdir(parents=True, exist_ok=True) 

booklist = 'all'
config = baseDir + '/support/oeb.config'
buildId = 'oeb-working'

##############################
#
#   Update USFM and RTF
#
##############################

tags = 'us-nrsv-neut-gehenna-ioudaioi-working'
swap = ''
usfmDir   = baseDir + 'artifacts/us/usfm'
rtfDir    = baseDir + 'artifacts/us/rtf'
indexDir  = baseDir + 'artifacts/us'
for d in [usfmDir, rtfDir, indexDir]: pathlib.Path(d).mkdir(parents=True, exist_ok=True) 
updateUSFM()

tags = 'cth-nrsv-neut-gehenna-ioudaioi-working'
swap = '--punctuation'
usfmDir   = baseDir + 'artifacts/cth/usfm'
rtfDir    = baseDir + 'artifacts/cth/rtf'
indexDir  = baseDir + 'artifacts/cth'
for d in [usfmDir, rtfDir, indexDir]: pathlib.Path(d).mkdir(parents=True, exist_ok=True) 
updateUSFM()

shutil.rmtree(tempDir)







