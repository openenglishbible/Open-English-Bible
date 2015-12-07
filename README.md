Open English Bible
==================

About
-----

The Open English Bible is the anticipated end product of a project intended to create an English translation of the Bible that is:

* under a licence enabling the maximum reuse, remixing and sharing without requiring the payment of royalties or the obtaining of permission from copyright holders; and
* a translation reflecting modern English usage and Biblical scholarship.

The New Testament of the OEB is being formed by editing the public domain Twentieth Century New Testament, which was a new translation of the New Testament published in the early twentieth century, based on the Greek text of Westcott and Hort.

The Hebrew Bible is being formed by editing a number of public domain translations done by John E McFadyen and Charles F Kent.

As such, the OEB as a translation does not stand within the Tyndale tradition but has a separate tradition in a similar manner to the NIV and New English Bible.

Our website is at http://openenglishbible.org

This site
---------

This source tree contains:

usfm/
The final generated usfm. This is probably what you want if you want to use the OEB's usfm files. The subdirectories are release/ which has the books in the OEB release, and development/ which has all books, no matter how partial or rough. 

source/
These are the source files we are working from. They are USFM files with a layer of markup to handle variations.

scratch/
These are various support documents such as books not yet fit for the development version.

build.py
The python 2.x script which creates a set of USFM files from the usfm.db files

build-standard.sh
Shell script which builds the main sets of USFM files in usfm/





