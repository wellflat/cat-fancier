#!/usr/bin/env sh

DATA=./data
IMAGEDIR=$DATA/cat_images_resize

mogrify -resize 256x256\! $IMAGEDIR/*.jpg
