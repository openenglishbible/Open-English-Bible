#!/bin/bash

build() {
	$USFMTOOLS/usfm-tools transform --target=$TARGET --usfmDir=$OEBDIR --builtDir=$BUILTDIR --config=$CONFIG --name=$ID
}

build-all(){

	rm -rf "$BUILTDIR"
	mkdir -p "$BUILTDIR"
	
	OEBDIR=$BUILTDIR/usfm
	mkdir -p $OEBDIR

	$USFMTOOLS/usfm-tools variant -s $SOURCEDIR -d $OEBDIR -t $TAGS -b $BOOKLIST $SWAP

	$USFMTOOLS/usfm-tools check -s $OEBDIR

	TARGET=md            ; build
	TARGET=singlehtml    ; build
	TARGET=rtf           ; build
	TARGET=html          ; build
	TARGET=epub          ; build
	TARGET=context       ; build
	TARGET=accordance    ; build
	TARGET=mobi          ; build
}

PYTHON=python3
SOURCEDIR=$PWD/source
CONFIG=$PWD/support/oeb.config
USFMTOOLS=USFM-Tools

ID=OEB-2022.1-US

BUILTDIR=$PWD/artifacts/us-release
TAGS=us-nrsv-neut-gehenna-ioudaioi
BOOKLIST=$PWD/books-in-release
SWAP=
build-all

ID=OEB-2022.1-Cth

BUILTDIR=$PWD/artifacts/cth-release
TAGS=cth-nrsv-neut-gehenna-ioudaioi
BOOKLIST=$PWD/books-in-release
SWAP=--punctuation
build-all
