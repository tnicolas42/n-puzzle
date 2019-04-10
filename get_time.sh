#!/bin/zsh

# usage
# ./get_time <puzzle-file> <npuzzle_path> <npuzzle_arg>
# ./get_time.sh ./test/all_tests/test3.15.puzzle npuzzle.py '--heuristic=manhattan'

npuzzle='npuzzle.py'
if [[ "$2" != "" ]]; then
    npuzzle="$2"
fi
result=`(time python3 $npuzzle $1 $3)  2>&1 >/dev/null | grep "python" | rev | awk '{print $8}' | rev | rev | cut -c 2- | rev`
echo $result

exit 0