#!/bin/bash


test=$(cat ./test)
for ligne in $test
do
    if [ $ligne -eq -1 ]
    then
        echo $ligne
    fi

done