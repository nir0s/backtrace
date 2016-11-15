# SOON!
# You should run this like so: `python test.py | backtrace`
# backtrace.py should capture stdin from the pipe and parse it,
# after which it should print it nicely.

import test2
import backtrace


backtrace.hook(
    reverse=False,
    align=True,
    strip_path=True,
    enable_on_envvar_only=False, conservative=True,
    on_tty=True, styles={})


class MyClass(object):
    def __init__(self):
        self.func_func_func_func_func_func_func()

    def func_func_func_func_func_func_func(self):
        _func()























































































def _func():
    test2._func2()


if __name__ == '__main__':
    i = MyClass()
