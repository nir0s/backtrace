# You should run this like so: `python test.py | backtrace`
# backtrace.py should capture stdin from the pipe and parse it,
# after which it should print it nicely.


def _func2():
    raise Exception()


def _func():
    _func2()


_func()
