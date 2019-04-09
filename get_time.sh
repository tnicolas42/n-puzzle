#!/bin/zsh

result=`(time python3 npuzzle.py $1)  2>&1 >/dev/null | grep "python" | awk '{print $4}'`
echo $result

exit 0