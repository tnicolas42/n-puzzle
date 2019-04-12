# n-puzzle [[42](https://www.42.fr/) project]

## Project
The goal of this project is to solve the N-puzzle ("taquin" in French) game using the A*
search algorithm or one of its variants.

See more on the [subject](https://github.com/tnicolas42/n-puzzle/blob/master/npuzzle.pdf).

## Usage
```
usage: npuzzle.py [-h] [--heuristic {manhattan,hamming,linear_conflict}] [-s]
                  [--silent] [--disable-auto-update] [-r RANDOM]
                  [--generate-solvable] [--generate-unsolvable] [-u] [-g] [-f]
                  [puzzle]

positional arguments:
  puzzle                The file that contain the puzzle

optional arguments:
  -h, --help            show this help message and exit
  --heuristic {manhattan,hamming,linear_conflict}
                        This is the heuristic function
  -s, --stats           Print stats about functions [for debug]
  --silent              Don't display all the puzzles states on the output
  --disable-auto-update
                        Disable the auto update of heuristic
  -r RANDOM, --random RANDOM
                        Generate a random puzzle of a given size
  --generate-solvable   Generate only solvable puzzle
  --generate-unsolvable
                        Generate only unsolvable puzzle
  -u, --uniform-cost    Set an uniform cost (heuristic funcion return 0) ->
                        it's like dijkstra
  -g, --greedy          Go to only one path, used to find a solution very
                        quickly but it's not the better path
  -f, --super-fast      Super fast algoritm -> just ignore the distance from
                        start
```
Example
```
python3 npuzzle.py test/all_tests/test3.12.puzzle --heuristic linear_conflict --slient
```
Return
```
base puzzle:
5   1
4   3   7
8   2   6
result:
1   2   3
8       4
7   6   5
all moves (26): BLLTRRBLTRBBLTLBRRTLBRTTLB
max opened at the same time: 722
total opened: 2007 -> using linear_conflict
```

## Generate puzzle
To generate puzzle:
```bash
python generator.py 3  # generate a puzzle of size 3*3
```

```bash
python generator 4 -s  # generate only solvable puzzle
python generator 4 -u  # generate only unsolvable puzzle
```

## Test the A* speed
This script can be used to test the A* algo
```
python3 mean_time.py <size> [--heuristic HEURISTIC] [--path PATH]
python3 mean_time.py 3
python3 mean_time.py 3 --heuristic manhattan --path test/all_tests
```
Return
```
test3.0.puzzle: 0.3s
test3.1.puzzle: 0.06s
test3.10.puzzle: 0.16s
test3.11.puzzle: 0.1s
test3.12.puzzle: 1.37s
test3.13.puzzle: 0.4s
test3.14.puzzle: 0.35s
test3.15.puzzle: 0.19s
test3.16.puzzle: 0.08s
test3.17.puzzle: 0.09s
test3.18.puzzle: 0.29s
test3.19.puzzle: 0.33s
test3.2.puzzle: 0.65s
test3.3.puzzle: 0.73s
test3.4.puzzle: 0.13s
test3.5.puzzle: 0.1s
test3.6.puzzle: 0.92s
test3.7.puzzle: 0.09s
test3.8.puzzle: 0.19s
test3.9.puzzle: 0.92s

summary for 20 files using linear_conflict
total time: 0m 7.45s
mean time: 0.37s
max time: 1.37s
min time: 0.06s
```

## Tests
To run tests:
```
nosetests
nosetests -v  # verbose mode
nosetests --nocapture  # show print
```
