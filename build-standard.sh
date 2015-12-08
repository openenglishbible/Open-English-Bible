#!/bin/sh

python build.py -s source -d usfm/release/us -t us-nrsv-neut-gehenna-ioudaioi -b books-in-release
python build.py -s source -d usfm/release/cth -t cth-nrsv-neut-gehenna-ioudaioi -b books-in-release

python build.py -s source -d usfm/development/us -t us-nrsv-neut-gehenna-ioudaioi
python build.py -s source -d usfm/development/cth -t cth-nrsv-neut-gehenna-ioudaioi

