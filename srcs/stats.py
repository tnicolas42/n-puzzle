#!/usr/bin/python3
import time

"""
Get stats on functions (nb time called, total exec time, mean exec time, ...)
To add stats on a funcion, just add a decorator get_stats:
>>> @get_stats
... def function():
...     pass
At the end of your prgm, print all the stats with the function print_stats()
>>> print_stats()
To enable/disable stats, change the value of EnableStats.stats
>>> EnableStats.stats = True
"""


class EnableStats:
    enable = False
    stats = None


def get_stats(function):
    if EnableStats.stats is None:
        EnableStats.stats = dict()
    EnableStats.stats[function.__name__] = dict(
        module=function.__module__,
        nb_call=0,
        total_time=0,
    )

    def decorator(*args, **kwargs):
        if not EnableStats.enable:
            return function(*args, **kwargs)
        EnableStats.stats[function.__name__]['nb_call'] += 1
        time_start = time.time()
        ret = function(*args, **kwargs)
        EnableStats.stats[function.__name__]['total_time'] += time.time() - time_start
        return ret
    return decorator


def print_stats():
    if EnableStats.stats is None or not EnableStats.enable:
        return
    for key in EnableStats.stats:
        val = EnableStats.stats[key]
        print('%s.py -> %s():' % (val['module'], key))
        print('\tfunction called %d times' % (val['nb_call']))
        if val['nb_call'] > 0:
            print('\ttotal exec time %fs' % (val['total_time']))
            print('\tmean time %fs' % (val['total_time'] / val['nb_call']))
