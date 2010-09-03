cat ../built/Bible.txt | tr [:upper:] [:lower:] | sed 's/[^[:alpha:]][^[:alpha:]]*/\
/g' | sort | uniq -c > wordlist