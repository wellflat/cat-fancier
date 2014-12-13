#!/usr/bin/env sh
# This script converts the cat data into leveldb format.

TOOLS=../../caffe/build/tools
TRAINDB=catnet_train_lmdb
TESTDB=catnet_val_lmdb
MEANFILE=catnet_mean.binaryproto
DATA=./data

echo "Creating train/test databases ..."

if [ -e $TRAINDB ];then
  rm -rf $TRAINDB
fi
if [ -e $TESTDB ];then
  rm -rf $TESTDB
fi
if [ -e $DATA/$MEANFILE ];then
  rm $DATA/$MEANFILE
fi

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=256 \
    --resize_width=256 \
    --shuffle \
    $DATA/ \
    $DATA/train.txt \
    $TRAINDB

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=256 \
    --resize_width=256 \
    --shuffle \
    $DATA/ \
    $DATA/val.txt \
    $TESTDB

echo "Creating mean file ..."

$TOOLS/compute_image_mean $TRAINDB $DATA/$MEANFILE

echo "Done."
