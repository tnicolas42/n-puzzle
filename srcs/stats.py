import time

enable_stats = True
stats = None


def get_stats(function):
    global stats
    global enable_stats
    if enable_stats:
        if stats is None:
            stats = dict()
        stats[function.__name__] = dict(
            module=function.__module__,
            nb_call=0,
            total_time=0,
        )

    def decorator(*args, **kwargs):
        if not enable_stats:
            return function(*args, **kwargs)
        stats[function.__name__]['nb_call'] += 1
        time_start = time.time()
        ret = function(*args, **kwargs)
        stats[function.__name__]['total_time'] += time.time() - time_start
        return ret
    return decorator


def print_stats():
    if stats is None:
        return
    for key in stats:
        val = stats[key]
        print('%s.py -> %s():' % (val['module'], key))
        print('\tfunction called %d times' % (val['nb_call']))
        if val['nb_call'] > 0:
            print('\ttotal exec time %fs' % (val['total_time']))
            print('\tmean time %fs' % (val['total_time'] / val['nb_call']))
