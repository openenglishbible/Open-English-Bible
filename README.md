Open English Bible
==================

About
-----

The Open English Bible is the anticipated end product of a project intended to create an English translation of the Bible that is:

* under a licence enabling the maximum reuse, remixing and sharing without requiring the payment of royalties or the obtaining of permission from copyright holders; and
* a translation reflecting modern English usage and Biblical scholarship.

The OEB is being formed by editing the public domain Twentieth Century New Testament, which was a new translation of the New Testament published in the early twentieth century, based on the Greek text of Westcott and Hort.

As such, the OEB as a translation does not stand within the Tyndale tradition but has a separate tradition in a similar manner to the NIV and New English Bible.

Our website is at http://openenglishbible.org

This site
---------

This source tree contains:

final-usfm/
The final generated usfm. This is probably what you want if you want to use the OEB's usfm files.

sources/
These are the source English translations we are working from.

staging/
These are altered usfm files.

patches/
These are changes to be automatically applied by build.py to the files in staging, and then copied to final-usfm

build.py
The python 2.x script to do the patching.



