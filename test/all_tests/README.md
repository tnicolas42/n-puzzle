# Create tests files
```
python ../../generator.py <size> -s > <file>
python ../../generator.py 3 -s > test3.1.puzzle
python ../../generator.py 4 -s -i 100 > test100-4.1.puzzle
```

Naming file:
```
test<nb_iteration>-<size>.<id>.puzzle
nb_iteration = number of iterations if specified in the generator
size = size of the puzzle
id = id of the file (0, 1, 2, ...)
```
