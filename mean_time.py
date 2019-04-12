#!/usr/bin/python3
import re
import os
import sys
import argparse
import subprocess

"""
python3 mean_time.py <size> [--path DIR_WITH_TESTS] [--heuristic HEURISTIC]
>>> python3 mean_time.py 3 --heuristic=manhattan
>>> python3 mean_time.py 3
>>> python3 mean_time.py 3 --heuristic=manhattan --path test/all_tests
"""


base = "/".join(sys.argv[0].split('/')[:-1])
if base == "":
    base = "./"
else:
    base += "/"

PATH_TEST = base + 'test/all_tests'
GET_TIME = base + "get_time.sh"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("size", type=int, help="Size of the puzzle -> must be > 3")
    parser.add_argument("--path", type=str, default=PATH_TEST, help="the folder with examples")
    parser.add_argument("--heuristic", type=str, default="linear_conflict",
                        help="This is the heuristic function")
    args = parser.parse_args()

    size_test = args.size
    PATH_TEST = args.path

    all_times = []
    files_to_test = os.listdir(PATH_TEST)
    for file in files_to_test:
        if re.match(r'.*' + str(size_test) + '\.\d*\.puzzle', file):
            print(end=file + ": ")
            sys.stdout.flush()
            command = GET_TIME + " " + PATH_TEST + '/' + file + " " + (base if base is not "./" else "") + \
                      "npuzzle.py '--heuristic=" + args.heuristic + "'"
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            output = output.decode("utf-8").strip()
            p_status = p.wait()

            out_min_sec = str(output).split(':')
            if len(out_min_sec) >= 2:
                cur_time = 60 * float(out_min_sec[0]) + float(out_min_sec[1])
            else:
                cur_time = float(out_min_sec[0])
            all_times.append(cur_time)
            print(str(cur_time) + 's')

    total_time = 0
    for t in all_times:
        total_time += t
    print("\nsummary for %d files using %s" % (len(all_times), args.heuristic))
    print("total time: %dm %.2fs" % (int(total_time // 60), total_time % 60))
    print("mean time: %.2fs" % (total_time / len(all_times)))
    print("max time: %.2fs" % (max(all_times)))
    print("min time: %.2fs" % (min(all_times)))
