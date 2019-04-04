#! /usr/bin/env bash
#build library py from ui

src=(
	'rsrc'
	)
ui='./ui'
lib_widget='./lib_widget'
for i in ${src[@]} ; do
	 cmd="$ui/$i.ui -o $lib_widget/$i.py"
	 echo $cmd
	 pyuic5 $cmd
done
