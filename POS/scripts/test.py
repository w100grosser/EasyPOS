def _test(**args):
    print(args, type(args))

_test(a = 1, v = 2)

f = {}
f["A"] = 2
f["cv"] = 3

_test(**f)