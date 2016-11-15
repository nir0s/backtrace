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
    enable_on_envvar_only=False, conservative=False,
    on_tty=True, styles={})


class Moose(object):
    def __init__(self):
        self.a_moose_once_bit_my_sister()

    def a_moose_once_bit_my_sister(self):
        _mynd_you()























































































def _mynd_you():
    test2.moose_bites_kan_be_pretty_nasti()


if __name__ == '__main__':
    i = Moose()
