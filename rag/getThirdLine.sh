#!/bin/bash

for file in "$@"; do
    if [ -f "$file" ]; then
        line=$(sed -n '3p' "$file")
        echo "$file: $line"
    else
        echo "$file: ERROR - no existe"
    fi
done
