#!/usr/bin/env sh
# This script converts the cat data into leveldb format.

TOOLS=../caffe/build/tools
DATA=./data

echo "Creating leveldb..."

rm -rf catnet_train_leveldb
rm -rf catnet_val_leveldb

RESIZE=true
GLOG_logtostderr=1 $TOOLS/convert_imageset.bin \
    $DATA/ \
    $DATA/train.txt \
    catnet_train_leveldb 1

GLOG_logtostderr=1 $TOOLS/convert_imageset.bin \
    $DATA/ \
    $DATA/val.txt \
    catnet_val_leveldb 1

echo "Computing image mean..."

$TOOLS/compute_image_mean.bin ./catnet_train_leveldb $DATA/catnet_mean.binaryproto

echo "Done."
