#!/bin/sh

BASEPATH=$1

find $BASEPATH -name "*txt" | sed 's/\....$//' | sort > /tmp/2
find $BASEPATH -name "*jpg" | sed 's/\....$//' | sort > /tmp/1

for f in $(comm -3 /tmp/1 /tmp/2 | grep -v classes); do
	rm -v $f.*
done

