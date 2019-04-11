#!/bin/sh

python generator.py $@ > tmp.puzzle
cat tmp.puzzle
echo "=============="
time python3 npuzzle.py tmp.puzzle
rm tmp.puzzle
