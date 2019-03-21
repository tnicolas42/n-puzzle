# n-puzzle [[42](https://www.42.fr/) project]

## Project
The goal of this project is to solve the N-puzzle ("taquin" in French) game using the A*
search algorithm or one of its variants.

See more on the [subject](https://github.com/tnicolas42/n-puzzle/blob/master/npuzzle.pdf).

## Generate puzzle
To generate puzzle:
```bash
python generator.py 3  # generate a puzzle of size 3*3
```

```bash
python generator 4 -s  # generate only solvable puzzle
python generator 4 -u  # generate only unsolvable puzzle
```

## Tests
To run tests:
```
nosetests
nosetests -v  # verbose mode
nosetests --nocapture  # show print
```
