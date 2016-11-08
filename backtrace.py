import sys
import traceback

from colorama import Fore, Style


def rehook(reverse=False):

    def new_excepthook(tpe, value, tb):
        # traceback.print_exception(
        #     etype=tpe,
        #     value=value,
        #     tb=tb)
        stack_trace_entries = traceback.extract_tb(tb)
        if reverse:
            stack_trace_entries = stack_trace_entries[::-1]
        for entry in stack_trace_entries:
            file = Style.DIM + '(' + entry[0] + ') '
            line = Fore.RED + str(entry[1])
            context = Fore.GREEN + ' Where: ' + \
                (entry[2] if entry[2] != "<module>" else __file__)
            call = Fore.YELLOW + ' --> ' + entry[3]
            sys.stdout.write(file + line + context + call)
            sys.stdout.flush()
            print(Style.RESET_ALL)
    sys.excepthook = new_excepthook


rehook(reverse=True)


def _func2():
    raise Exception()


def _func():
    _func2()


if __name__ == '__main__':
    _func()
