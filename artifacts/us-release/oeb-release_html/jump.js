    $( document ).ready(function() {
 
        $( "html" ).click(function( e ) {
            var container = $("navtable");
            if (!container.is(e.target)
                && container.has(e.target).length === 0) 
            {
                container.css( "left", "-99999px" ); 
            }           
         });
        
        $( "#navbar" ).click(function( event ) {
           if (screen.width < 500) {
               window.location.href = 'index.html';
               //window.open(newPosition);
               return false;
           };
           $("#navtable").css( "left", "0px" );
        });
 
        $( "#navbar" ).hover(
            function( e ) {
                 if (screen.width < 500) {
                     return false;
                 };
                 $("#navtable").css( "left", "0px"    ); },
            function( e ) {
                 if (screen.width < 500) {
                     return false;
                 };
                 $("#navtable").css( "left", "-99999px" ); }
        );
        
        $("#navform").submit(function() {
            var bookNames = {
                'Hk':           '035',
                'Jn':           '043',
                'Js':           '059',
                'Mt':           '040',
                'Cl':           '051',
                'Jb':           '018',
                'Jg':           '007',
                '1Jn':          '062',
                '2Jn':          '063',
                '3Jn':          '064',
                'Lk':           '042',
                '1Tm':          '054',
                '2Tm':          '055',
                'Zp':           '036',
                'Er':           '015',
                'Hg':           '037',
                'Jd':           '065',
                'Jl':           '029',
                'Mk':           '041',
                'Pm':           '057',
                'Tt':           '056',
                'Dn':           '027',
                'Dt':           '005',
                'Gn':           '001',
            'Genesis':          '001',
            'Exodus':           '002',
            'Leviticus':        '003',
            'Numbers':          '004',
            'Deuteronomy':      '005',
            'Joshua':           '006',
            'Judges':           '007',
            'Ruth':             '008',
            '1Samuel':          '009',
            '2Samuel':          '010',
            '1Kings':           '011',
            '2Kings':           '012',
            '1Chronicles':      '013',
            '2Chronicles':      '014',
            'Ezra':             '015',
            'Nehemiah':         '016',
            'Esther':           '017',
            'Job':              '018',
            'Psalms':           '019',
            'Proverbs':         '020',
            'Ecclesiastes':     '021',
            'Song of Solomon':  '022',
            'Isaiah':           '023',
            'Jeremiah':         '024',
            'Lamentations':     '025',
            'Ezekiel':          '026',
            'Daniel':           '027',
            'Hosea':            '028',
            'Joel':             '029',
            'Amos':             '030',
            'Obadiah':          '031',
            'Jonah':            '032',
            'Micah':            '033',
            'Nahum':            '034',
            'Habakkuk':         '035',
            'Zephaniah':        '036',
            'Haggai':           '037',
            'Zechariah':        '038',
            'Malachi':          '039',
            'Matthew':          '040',
            'Mark':             '041',
            'Luke':             '042',
            'John':             '043',
            'Acts':             '044',
            'Romans':           '045',
            '1Corinthians':     '046',
            '2Corinthians':     '047',
            'Galatians':        '048',
            'Ephesians':        '049',
            'Philippians':      '050',
            'Colossians':       '051',
            '1Thessalonians':   '052',
            '2Thessalonians':   '053',
            '1Timothy':         '054',
            '2Timothy':         '055',
            'Titus':            '056',
            'Philemon':         '057',
            'Hebrews':          '058',
            'James':            '059',
            '1Peter':           '060',
            '2Peter':           '061',
            '1John':            '062',
            '2John':            '063',
            '3John':            '064',
            'Jude':             '065',
            'Revelation':       '066'
            };

                // get reference string
                var raw = $("#txtSearch").val();
                // split into words
                var spt = raw.split(/[\s,:]+/); 
                // filter junk words
                spt = spt.filter(function(val) { return /[^\s]+/.test(val) });
                // pad to make sure we end up somewhere OK
                spt = spt.concat(['001', '001', '001']);
                // merge split names eg 1 John -> 1John
                if (/[1234]+/.test(spt[0])) { spt[0] = spt[0] + spt[1] ; spt[1] = spt[2] ; spt[2] = spt[3]};
                // set chapter verse offset
                var offset = "001".substring(0, 3 - spt[1].length) + spt[1] + "001".substring(0, 3 - spt[2].length) + spt[2];
                var book = '040' // Matthew
                // lookup book number
                for (var key in bookNames) {
                    if (key.substring(0,spt[0].length).toLowerCase() === spt[0].toLowerCase()) {
                        book = bookNames[key];
                        break;
                    }
                }
                // Hide popup
                $("table").css( "left", "-99999px" ); 
                // Jump to new position
                var newPosition = "b" + book + ".html#" + offset;
                window.location.href = newPosition;
                //window.open(newPosition);
                return false;
        });

    });
