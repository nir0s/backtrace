import os
import sys
import traceback
from os.path import basename

import colorama
from colorama import Fore, Style


# TODO: Allow to enable backtrace by setting an environment variable.

RESET = Style.RESET_ALL

STYLES = {
    'backtrace': Fore.YELLOW + '{0}',
    'error': Fore.RED + Style.BRIGHT + '{0}',
    'line': Fore.RED + Style.BRIGHT + '{0}',
    'module': '{0}',
    'context': Style.BRIGHT + Fore.GREEN + '{0}',
    'call': Fore.YELLOW + ' --> ' + Style.BRIGHT + '{0}',
}


def _flush(message):
    sys.stderr.write(message + '\n')
    sys.stderr.flush()


class _Hook(object):
    def __init__(self,
                 entries,
                 align=False,
                 strip_path=False):
        self.entries = entries
        self.align = align
        self.strip = strip_path

    def reverse(self):
        self.entries = self.entries[::-1]

    def rebuild_entry(self, entry, styles):
        module = basename(entry[0]) if self.strip else entry[0]
        return (
            styles['line'].format(str(entry[1])) + RESET,
            styles['module'].format(module) + RESET,
            styles['context'].format(entry[2]) + RESET,
            styles['call'].format(entry[3]) + RESET
        )

    @staticmethod
    def align_all(entries):
        lengths = [0, 0, 0, 0]

        for entry in entries:
            for index, field in enumerate(entry):
                lengths[index] = max(lengths[index], len(str(field)))
        return lengths

    @staticmethod
    def align_entry(entry, lengths):
        return ' '.join(
            ['{0:{1}}'.format(field, lengths[index])
             for index, field in enumerate(entry)])

    def generate_backtrace(self, styles):
        """Return the (potentially) aligned, rebuit traceback

        Yes, we iterate over the entries thrice. We sacrifice
        performance for code readability. I mean.. come on, how long can
        your traceback be that it matters?
        """
        backtrace = []
        for entry in self.entries:
            backtrace.append(self.rebuild_entry(entry, styles))

        # Get the lenght of the longest string for each field of an entry
        lengths = self.align_all(backtrace) if self.align else [1, 1, 1, 1]

        aligned_backtrace = []
        for entry in backtrace:
            aligned_backtrace.append(self.align_entry(entry, lengths))
        return aligned_backtrace


def hook(reverse=False,
         align=False,
         strip_path=False,
         enable_on_envvar_only=False,
         on_tty=False,
         styles=None):
    """Hook the current excepthook to the backtrace.

    If `align` is True, all parts (line numbers, file names, etc..) will be
    aligned to the left according to the longest entry.

    If `strip_path` is True, only the file name will be shown, not its full
    path.

    If `enable_on_envvar_only` is True, only if the environment variable
    `ENABLE_BACKTRACE` is set, backtrace will be activated.

    If `on_tty` is True, backtrace will be activated only if you're running
    in a readl terminal (i.e. not piped, redirected, etc..).

    See https://github.com/nir0s/backtrace/blob/master/README.md for
    information on `styles`.
    """
    if enable_on_envvar_only and 'ENABLE_BACKTRACE' not in os.environ:
        return

    isatty = getattr(sys.stderr, 'isatty', lambda: False)
    if on_tty and not isatty():
        return

    if styles:
        # TODO: When removing support for py26, change to dict comprehension
        for k in STYLES.keys():
            styles[k] = styles.get(k, STYLES[k])
    else:
        styles = STYLES

    colorama.init(autoreset=True)

    def backtrace_excepthook(tpe, value, tb):
        traceback_entries = traceback.extract_tb(tb)
        hook = _Hook(traceback_entries, align=align, strip_path=strip_path)

        backtrace_message = styles['backtrace'].format(
            'Traceback ({0}):'.format(
                'Most recent call first' if reverse
                else 'Most recent call last'))
        error_message = styles['error'].format('{0}: {1}'.format(
            tpe.__name__, str(value)))

        _flush(backtrace_message)

        if reverse:
            hook.reverse()

        backtrace = hook.generate_backtrace(styles)
        backtrace.insert(0 if reverse else len(backtrace), error_message)
        for entry in backtrace:
            _flush(entry)

    sys.excepthook = backtrace_excepthook


def unhook():
    """Restore the default excepthook
    """
    sys.excepthook = sys.__excepthook__
