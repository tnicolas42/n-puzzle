import os
from srcs.parser import parse_from_file

PATH_VALID = 'test/valid/'
PATH_INVALID = 'test/invalid/'
FILES_INVALID_TO_TEST = ['/dev/null', 'filenotfound', '~/.Trashes']

def test_valid():
    files_to_test = os.listdir(PATH_VALID)
    for f in files_to_test:
        f = PATH_VALID + '/' + f
        if os.path.isfile(f):
            puzzle = parse_from_file(f)
            if puzzle is None:
                raise Exception("puzzle is None with a valid file (%s)" % (f))
            print("check with %s -> OK" % (f))

def test_invalid():
    files_to_test = os.listdir(PATH_INVALID)
    for f in files_to_test:
        f = PATH_INVALID + '/' + f
        if os.path.isfile(f):
            puzzle = parse_from_file(f)
            if puzzle is not None:
                raise Exception("puzzle is not None with an ivalid file (%s)" % (f))
            print("check with %s -> OK" % (f))
    files_to_test = FILES_INVALID_TO_TEST
    for f in files_to_test:
        puzzle = parse_from_file(f)
        if puzzle is not None:
            raise Exception("puzzle is not None with an ivalid file (%s)" % (f))
        print("check with %s -> OK" % (f))
