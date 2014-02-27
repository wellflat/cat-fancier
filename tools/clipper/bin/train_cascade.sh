#!/bin/sh

#    /usr/local/bin/opencv_createsamples -info positive.dat -vec positive.vec -num $1
#    /usr/local/bin/opencv_createsamples -vec yahoo_88_24.vec -img static/images/yahoo/yahoo-japan.jpg -bg negative.dat -num 2000 -bgcolor 255 -w 88 -h 24

time opencv_traincascade -data $DST_DIR -vec $VEC_FILE -bg $BG_FILE -numPos $1 -numNeg $2 -featureType LBP -maxFalseAlarmRate 0.4 > train.log
