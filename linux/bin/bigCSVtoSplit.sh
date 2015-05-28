#!/bin/bash

awk 'BEGIN {cnt=0;ncnt=0}{FS=","}{if ($1 != prev) { cnt+=1; prev=$1; };if (cnt<10) {print $0 > "vmdata"ncnt".csv"} else {cnt=0;ncnt+=1}}' out.csv

ls vmdata*csv | while read x; do cat header | cat - $x > tt && mv tt $x; done
