import os
import sys
import traceback
from os.path import basename

import colorama
from colorama import Fore, Style


# TODO: Allow to enable backtrace by setting an environment variable.


def _flush(message):
    sys.stderr.write(message + '\n')
    sys.stderr.flush()


class _Hook(object):
    def __init__(self,
                 entries,
                 align=False,
                 strip_path=False):
        self.entries = entries
        self._align = align
        self._strip = strip_path

    def reverse(self):
        self.entries = self.entries[::-1]

    def generate_backtrace(self,
                           line_format=None,
                           file_format=None,
                           context_format=None,
                           call_format=None):
        line_format = line_format or (Fore.RED + Style.BRIGHT)
        file_format = file_format or ''
        context_format = context_format or (Style.BRIGHT + Fore.GREEN)
        call_format = call_format or (Fore.YELLOW + ' --> ' + Style.BRIGHT)

        rebuilt_traceback = []
        for entry in self.entries:
            rebuilt_traceback.append((
                line_format + str(entry[1]) + Style.RESET_ALL,
                file_format + (basename(
                    entry[0]) if self._strip else entry[0]) + Style.RESET_ALL,
                context_format + entry[2] + Style.RESET_ALL,
                call_format + entry[3] + Style.RESET_ALL))

        lengths = self.set_alignment(rebuilt_traceback) if \
            self._align else [1, 1, 1, 1]

        backtrace_entries = []
        for entry in rebuilt_traceback:
            backtrace_entries.append(' '.join(
                ['{0:{1}}'.format(field, lengths[index])
                 for index, field in enumerate(entry)]))
        return backtrace_entries

    def set_alignment(self, entries):
        lengths = [0, 0, 0, 0]

        for entry in entries:
            for index, field in enumerate(entry):
                lengths[index] = max(lengths[index], len(str(field)))
        return lengths


def hook(reverse=False,
         align=False,
         strip_path=False,
         enable_on_envvar_only=False,
         on_tty=False,
         line_format=None,
         file_format=None,
         context_format=None,
         call_format=None):
    """Hook the current excepthook to the backtrace.

    If `align` is True, all parts (line numbers, file names, etc..) will be
    aligned to the left according to the longest entry.

    If `strip_path` is True, only the file name will be shown, not its full
    path.

    If `enable_on_envvar_only` is True, only if the environment variable
    `ENABLE_BACKTRACE` is set, backtrace will be activated.

    If `on_tty` is True, backtrace will be activated only if you're running
    in a readl terminal (i.e. not piped, redirected, etc..).

    `line_format` is a formatting for the line number.
    `file_format` is a formatting for the file path.
    `context_format` is a formatting for the calling function/module.
    `call_format` is a formatting for the called function.
    """
    if enable_on_envvar_only and 'ENABLE_BACKTRACE' not in os.environ:
        return

    isatty = getattr(sys.stderr, 'isatty', lambda: False)
    if on_tty and not isatty():
        return

    colorama.init(autoreset=True)

    def backtrace_excepthook(tpe, value, tb):
        traceback_entries = traceback.extract_tb(tb)
        hook = _Hook(traceback_entries, align=align, strip_path=strip_path)

        backtrace_message = '{0}Traceback ({1}):'.format(
            Fore.YELLOW,
            'Most recent call first' if reverse
            else 'Most recent call last')
        error_message = '{0}{1}{2}: {3}'.format(
            Fore.RED,
            Style.BRIGHT,
            tpe.__name__,
            str(value))

        _flush(backtrace_message)

        if reverse:
            hook.reverse()

        backtrace = hook.generate_backtrace(
            line_format,
            file_format,
            context_format,
            call_format)
        backtrace.insert(0 if reverse else len(backtrace), error_message)
        for entry in backtrace:
            _flush(entry)

    sys.excepthook = backtrace_excepthook


def unhook():
    """Restore the default excepthook
    """
    sys.excepthook = sys.__excepthook__
