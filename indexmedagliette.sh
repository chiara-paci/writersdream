#!/bin/bash

DIR=/home/chiara/simplehtml/wd/medagliette


(
    sed 's/%%%TITLE%%%/Medagliette/g' templates/begin.html

    echo '<style>'
    echo 'section.type h1 { 
       text-align: center;
       border-bottom: 1px solid black;
    }'
    echo 'section.type h3 { 
       font-weight: normal;
       font-style: italic;
    }'
    echo '</style>'

    for f in $(find $DIR -type f)
    do
	fname=$( basename $f )
	case $fname in 
	    *big.png) continue;;
	    *pennaespada*)
		order="A"
		ftype=spec
		fsub=ps
		year="----"
		;;
	    *coppa*)
		order="A"
		ftype=spec
		fsub=nat
		year=2017
		;;
	    *mi100*) continue;;
	    MI2019*)
		order="B"
		ftype="mi"
		fsub="anno"
		year=2019
		;;
	    *rame-mi*|MI*)
		ftype="mi"
		fsub="normale"
		order="B"
		year="----"
		;;
	    *oro-mi*)
		order="B"
		ftype="mi"
		fsub="anno"
		year=$( echo $fname | sed 's/medagliette-oro-mi//g' | sed 's/.png//g' )
		;;
	    luna2019*)
		order="C"
		year=2019
		ftype=lune
		fsub="anno"
		;;
	    *argento-lune*)
		order="C"
		year=$( echo $fname | sed 's/medagliette-argento-lune//g' | sed 's/...png//g' )
		ftype=lune
		fsub="normale"
		;;
	    MR*)
		order="D"
		year=2019
		ftype=mr
		fsub="normale"
		;;
	    luna*)
		order="C"
		year=2019
		ftype=lune
		fsub="normale"
		;;
	    *oro-lune*)
		order="C"
		year=$( echo $fname | sed 's/medagliette-oro-lune//g' | sed 's/.png//g' )
		ftype=lune
		fsub="anno"
		;;
	    *halloween*)
		order="A"
		year=$( echo $fname | sed 's/medagliette-[a-z]*-halloween//g' | sed 's/.png//g' )
		ftype=spec
		fsub=hal
		;;
	    *fdi*)
		order="A"
		year=$( echo $fname | sed 's/medagliette-[a-z]*-fdi//g' | sed 's/.png//g' )
		ftype=spec
		fsub=fdi
		;;
	    estate_*)
		order="A"
		year=2019
		ftype=spec
		fsub=fdi
		;;
	    *befana*)
		order="A"
		year=$( echo $fname | sed 's/medagliette-[a-z-]*2/2/g' | sed 's/.png//g' )
		ftype=spec
		fsub=nat
		;;
	    *natale*)
		order="A"
		year=$( echo $fname | sed 's/medagliette-[a-z-]*2/2/g' | sed 's/.png//g' )
		if [ "$year" = 2017 ]
                then
                    continue
	        fi
		ftype=spec
		fsub=nat
		;;
	    *)
		continue
		;;
	esac
	echo $order $ftype $fsub $year $fname
    done | sort -n | awk '{ print $2" "$3" "$4" "$5 }' | awk -f med2html.awk
    cat templates/end.html

) > $DIR/index.html
