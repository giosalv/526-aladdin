#!/usr/bin/bash


if [ -z "$1" ] ;
then
	SRC_ROOT="."
else
	SRC_ROOT="$1"
fi

if [ -z "$2" ] ;
then
	DEST_ROOT="$HOME/workspace/uiuc/classes/cs526/s17/project/2/SHOC"
else
	DEST_ROOT="$2"
fi


if [ ! -e "$SRC_ROOT" ] || [ ! -d "$SRC_ROOT" ] ;
then
	echo "Source root '$SRC_ROOT' does not exist or is not a directory"
	exit 1
fi

if [ ! -e "$DEST_ROOT" ] || [ ! -d "$DEST_ROOT" ] ;
then
	echo "Destination root '$DEST_ROOT' does not exist or is not a directory"
	exit 1
fi


for file in $(find "$SRC_ROOT" -name '*.pdf')
do
	echo "Copying: $file"
	file_bname=$(basename "$file")
	cp "$file" "$DEST_ROOT/$file_bname"
done


exit 0
