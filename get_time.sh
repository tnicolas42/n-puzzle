#!/bin/zsh

npuzzle='npuzzle.py'
if [[ "$2" != "" ]]; then
    npuzzle="$2/$npuzzle"
fi
result=`(time python3 $npuzzle $1)  2>&1 >/dev/null | grep "python" | awk '{print $4}' | rev | cut -c 2- | rev`
echo $result

exit 0