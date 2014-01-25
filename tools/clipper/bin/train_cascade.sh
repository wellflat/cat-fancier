#!/bin/sh

CMD=/usr/local/bin/opencv_traincascade
DST_DIR=train/
VEC_FILE=positive.vec
BG_FILE=negative.dat
NUM_POS=
NUM_NEG=
#FEATURE_TYPE=LBP
FEATURE_TYPE=HAAR

function create_samples {
    /usr/local/bin/opencv_createsamples -info positive.dat -vec positive.vec -num $1
}

function main {
    if [ $# -ne 2 ]; then
        echo required 2 arguments [numpos/numneg]
        exit -1
    fi
    
    $CMD -data $DST_DIR -vec $VEC_FILE -bg $BG_FILE -numPos $1 -numNeg $2 -featureType $FEATURE_TYPE
}

main $*
