#!/bin/bash

for i in *.txt
do
    dirname=${i%.*}
    mkdir $dirname
#     name=${i#*.}
#     echo $i
#     echo "dirname is: $dirname"
#     echo "name is: $name"
    cp $i $dirname
done
