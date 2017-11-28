	#!/bin/bash

	build() {
		$PYTHON $USFMTOOLS/transform/transform.py --target=$TARGET --usfmDir=$OEBDIR --builtDir=$BUILTDIR --config=$CONFIG --name=$ID
	}

	build-all(){
	
		rm -rf "$BUILTDIR"
		mkdir -p "$BUILTDIR"
		
		OEBDIR=$BUILTDIR/usfm
		mkdir -p $OEBDIR

		$PYTHON $USFMTOOLS/variant/variant.py -s $SOURCEDIR -d $OEBDIR -t $TAGS -b $BOOKLIST $SWAP

		$PYTHON $USFMTOOLS/check/check.py -s $OEBDIR

		TARGET=md            ; build
		TARGET=singlehtml    ; build
		TARGET=rtf           ; build
		TARGET=html          ; build
		TARGET=epub          ; build
		TARGET=context       ; build
		TARGET=accordance    ; build
		TARGET=mobi          ; build
	}

	PYTHON=pypy3
	SOURCEDIR=$PWD/source
	CONFIG=$PWD/support/oeb.config
	USFMTOOLS=USFM-Tools

	ID=oeb-release

	BUILTDIR=$PWD/artifacts/us-release
	TAGS=us-nrsv-neut-gehenna-ioudaioi
	BOOKLIST=$PWD/books-in-release
	SWAP=
	build-all

	BUILTDIR=$PWD/artifacts/cth-release
	TAGS=cth-nrsv-neut-gehenna-ioudaioi
	BOOKLIST=$PWD/books-in-release
	SWAP=--punctuation
	build-all

	ID=oeb-working

	BUILTDIR=$PWD/artifacts/us-working
	TAGS=us-nrsv-neut-gehenna-ioudaioi
	BOOKLIST=all
	SWAP=
	build-all

	BUILTDIR=$PWD/artifacts/cth-working
	TAGS=cth-nrsv-neut-gehenna-ioudaioi
	BOOKLIST=all
	SWAP=--punctuation
	build-all	