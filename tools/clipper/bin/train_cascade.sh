#!/bin/sh

CMD=/usr/local/bin/opencv_traincascade
DST_DIR=train/haar
VEC_FILE=positive.vec
BG_FILE=negative.dat
NUM_POS=
NUM_NEG=
FEATURE_TYPE=LBP
#FEATURE_TYPE=HAAR
LOG_FILE=train.log

function create_samples {
    /usr/local/bin/opencv_createsamples -info positive.dat -vec positive.vec -num $1
#    /usr/local/bin/opencv_createsamples -vec yahoo_88_24.vec -img static/images/yahoo/yahoo-japan.jpg -bg negative.dat -num 2000 -bgcolor 255 -w 88 -h 24
}

function train_cascade {
    if [ $# -ne 2 ]; then
        echo required 2 arguments [numpos/numneg]
        exit -1
    fi
#    opencv_traincascade -data train/yahoo/lbp -vec yahoo_88_24.vec -numPos 1800 -bg negative.dat -numNeg 3937 -w 88 -h 24 -featureType LBP > train_logo.log    
    $CMD -data $DST_DIR -vec $VEC_FILE -bg $BG_FILE -numPos $1 -numNeg $2 -featureType $FEATURE_TYPE -maxFalseAlarmRate 0.4 > $LOG_FILE
}

train_cascade $*
