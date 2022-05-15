#!/bin/bash

dot_files=$(find -name "graphe[1-9]*.dot")

for file in $dot_files
    do
        id=$(echo $file | cut -d "e" -f 2 | cut -d "." -f 1)
        if [ $id -lt 10 ];
        then
            id="0$id"
        fi
        # echo $id
        png_file="graphe$id.png"
        # echo $svg_file
        dot -Kfdp -Tpng $file > png/$png_file
    done

# file="graphe2.dot"
# id=$(echo $file | cut -d "e" -f 2 | cut -d "." -f 1)
# echo $id
# svg_file="graphe${id}.svg"
# echo $svg_file