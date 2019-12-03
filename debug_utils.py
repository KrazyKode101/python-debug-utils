from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

count_calls = {}

@decorator
def countcalls(f):
    def _f(*args):
        count_calls[f] += 1
        return f(*args)
    count_calls[f] = 0
    return _f

@decorator
def memoize(f):
    print("memoize")
    cache = {}
    def _f(*args):
        nonlocal cache
        try:
            return cache[args]
        except KeyError:
            result = cache[args] = f(*args)
            return result
        except TypeError:
            return f(*args)
    print("_f memoize")
    return _f

@decorator
def trace(f):
    indent = '   '
    level = 0
    opfile = open("trace.txt",'w')
    def _f(*args):
        nonlocal level
        nonlocal opfile
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        opfile.write('%s--> %s\n' % (level*indent, signature))
        level += 1
        try:
            result = f(*args)
        finally:
            level -= 1
        opfile.write('%s<-- %s == %s\n' % ((level)*indent, signature, result))
        return result
    return _f

"""
def disabled(func): return func
trace = disabled
"""