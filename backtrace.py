import os
import sys
import traceback

import colorama
from colorama import Fore, Style


STYLES = {
    'backtrace': Fore.YELLOW + '{0}',
    'error': Fore.RED + Style.BRIGHT + '{0}',
    'line': Fore.RED + Style.BRIGHT + '{0}',
    'module': '{0}',
    'context': Style.BRIGHT + Fore.GREEN + '{0}',
    'call': Fore.YELLOW + '--> ' + Style.BRIGHT + '{0}',
}

CONVERVATIVE_STYLES = {
    'backtrace': Fore.YELLOW + '{0}',
    'error': Fore.RED + Style.BRIGHT + '{0}',
    'line': 'line ' + Fore.RED + Style.BRIGHT + '{0},',
    'module': 'File {0},',
    'context': 'in ' + Style.BRIGHT + Fore.GREEN + '{0}',
    'call': Fore.YELLOW + '--> ' + Style.BRIGHT + '{0}',
}


def _flush(message):
    sys.stderr.write(message + '\n')
    sys.stderr.flush()


class _Hook(object):
    def __init__(self,
                 entries,
                 align=False,
                 strip_path=False,
                 conservative=False):
        self.entries = entries
        self.align = align
        self.strip = strip_path
        self.conservative = conservative

    def reverse(self):
        self.entries = self.entries[::-1]

    def rebuild_entry(self, entry, styles):
        entry = list(entry)
        # This is the file path.
        entry[0] = os.path.basename(entry[0]) if self.strip else entry[0]
        # Always an int (entry line number)
        entry[1] = str(entry[1])

        new_entry = [
            styles['line'].format(entry[1]) + Style.RESET_ALL,
            styles['module'].format(entry[0]) + Style.RESET_ALL,
            styles['context'].format(entry[2]) + Style.RESET_ALL,
            styles['call'].format(entry[3]) + Style.RESET_ALL
        ]
        if self.conservative:
            new_entry[0], new_entry[1] = new_entry[1], new_entry[0]

        return new_entry

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
         conservative=False,
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

    If `convervative` is True, the traceback will have more seemingly original
    style (There will be no alignment by default, 'File', 'line' and 'in'
    prefixes and will ignore any styling provided by the user.)

    See https://github.com/nir0s/backtrace/blob/master/README.md for
    information on `styles`.
    """
    if enable_on_envvar_only and 'ENABLE_BACKTRACE' not in os.environ:
        return

    isatty = getattr(sys.stderr, 'isatty', lambda: False)
    if on_tty and not isatty():
        return

    if conservative:
        styles = CONVERVATIVE_STYLES
        align = align or False
    elif styles:
        for k in STYLES.keys():
            styles[k] = styles.get(k, STYLES[k])
    else:
        styles = STYLES

    # For Windows
    colorama.init(autoreset=True)

    def backtrace_excepthook(tpe, value, tb):
        traceback_entries = traceback.extract_tb(tb)
        hook = _Hook(traceback_entries, align, strip_path, conservative)

        tb_message = styles['backtrace'].format('Traceback ({0}):'.format(
            'Most recent call ' + 'first' if reverse else 'last'))
        err_message = styles['error'].format(tpe.__name__ + ': ' + str(value))

        if reverse:
            hook.reverse()

        _flush(tb_message)
        backtrace = hook.generate_backtrace(styles)
        backtrace.insert(0 if reverse else len(backtrace), err_message)
        for entry in backtrace:
            _flush(entry)

    sys.excepthook = backtrace_excepthook


def unhook():
    """Restore the default excepthook
    """
    sys.excepthook = sys.__excepthook__
