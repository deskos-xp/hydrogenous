#! /usr/bin/env bash
#build library py from ui

function filter(){
	basename "$(echo $1 | sed s/'\.ui'/''/g)"
}

src=()
for f in `ls -1 ui/*.ui` ; do 
	src+=("$(filter $f)")
done

ui='./ui'
lib_widget='./lib_widget'
for i in ${src[@]} ; do
	if test "$SHELL" = '/bin/bash' ; then 
		cmd="$ui/$i.ui -o $lib_widget/$i.py"
		echo $cmd
		pyuic5 $cmd
	elif test "$SHELL" = '/usr/bin/zsh' ; then
		IN="$ui/$i.ui"
		OUT="$lib_widget/$i.py"
		echo "$IN -o $OUT"
		pyuic5 "$IN" -o "$OUT"
	fi
done
