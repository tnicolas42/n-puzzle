#!/bin/sh

python generator.py $@ > tmp.puzzle
cat tmp.puzzle
echo "=============="
python3 npuzzle.py tmp.puzzle
