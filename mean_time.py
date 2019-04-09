#!/usr/bin/python3
import re
import os
import sys
import subprocess

PATH_TEST = 'test/valid/'

if __name__ == "__main__":
    size_test = int(sys.argv[1])

    files_to_test = os.listdir(PATH_TEST)
    for file in files_to_test:
        p = subprocess.Popen("./get_time.sh " + PATH_TEST + file, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        print(file + ": " + str(output))
