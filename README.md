backtrace
=========

WIP! Untested!


[![Travis Build Status](https://travis-ci.org/nir0s/backtrace.svg?branch=master)](https://travis-ci.org/nir0s/backtrace)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/khf9a98rbwp1ehfh/branch/master?svg=true)](https://ci.appveyor.com/project/nir0s/backtrace)
[![PyPI Version](http://img.shields.io/pypi/v/backtrace.svg)](http://img.shields.io/pypi/v/backtrace.svg)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/backtrace.svg)](https://img.shields.io/pypi/pyversions/backtrace.svg)
[![Requirements Status](https://requires.io/github/nir0s/backtrace/requirements.svg?branch=master)](https://requires.io/github/nir0s/backtrace/requirements/?branch=master)
[![Code Coverage](https://codecov.io/github/nir0s/backtrace/coverage.svg?branch=master)](https://codecov.io/github/nir0s/backtrace?branch=master)
[![Code Quality](https://landscape.io/github/nir0s/backtrace/master/landscape.svg?style=flat)](https://landscape.io/github/nir0s/backtrace)
[![Is Wheel](https://img.shields.io/pypi/wheel/backtrace.svg?style=flat)](https://pypi.python.org/pypi/backtrace)

backtrace manipulates Python tracebacks to make them more readable.
It provides different configuration options for coloring and formatting.

backtrace also allows to choose the formatting of each part of the traceback; show the traceback entries in reversed order, and more..

Example:

![Trump? REALLY?! What a nation of idiots!](https://github.com/nir0s/backtrace/raw/master/img/main.png)

NOTE: Didn't test this on Windows yet. Should work.. but don't know how well.


## Alternatives

* [colored_traceback](https://github.com/staticshock/colored-traceback.py) provides a way to color your tracebacks to make them more readable. It's a nice little tool but lacks actually re-formatting the traceback which is what the biggest problem is from my POV.
* Um.. your own implementation? There's really a reason for me doing this. I do have a life you know (well.. I try anyway).


## Installation

backtrace officially supports Linux and OSX on Python 2.7 and 3.4+. Python 2.6 will also probably work, but with no guarantees.

```shell
pip install backtrace
```

For dev:

```shell
pip install https://github.com/nir0s/backtrace/archive/master.tar.gz
```


## Usage

backtrace provides two methods for manipulating your tracebacks.

* Piping to backtrace using its CLI
* Using backtrace from within your code

### Piping

```bash
$ python my-program.py | backtrace # Soon...
```

### Inside your application

```python
import backtrace

backtrace.hook(
    reverse=False,
    align=False,
    strip_path=False,
    enable_on_envvar_only=False,
    on_tty=False,
    conservative=False,
    styles={})

# more code...

# if you wanna restore the default hook...
backtrace.unhook()
...

```

You can pass the following flags to `hook` to change backtrace's behavior:

* If `reverse` is True, the traceback entries will be printed in reverse order.
* If `align` is True, all parts (line numbers, file names, etc..) will be
aligned to the left according to the longest entry. This allow for extended readability as you eyes don't have to move between columns to understand what's going on.
* If `strip_path` is True, only the file name will be shown, not its full
path. This is useful when you know you're running in the context of a single module or a single package containing only a root folder so you only need file names. This can help keep the traceback clean.
* If `enable_on_envvar_only` is True, only if the environment variable
`ENABLE_BACKTRACE` is set, backtrace will be activated.
* If `on_tty` is True, backtrace will be activated only if you're running
in a real terminal (i.e. not piped, redirected, etc..). This can help keep the original traceback when logging to files or piping to look for information.
* `styles` is a dictionary containing the styling for each part of the rebuilt traceback. See below:
* If `conservative` is true, a more conservative view will be provided for people who find the default backtrace style too new or intimidating. For example, no alignment will be done (unless `align` is explicitly passed), `styles` will be ignored, and potential unnecessary data will be retained. Try It! It's still eye-candy.

#### Styles

Styles allow you to customize the coloring and structure of your new traceback. The defaults are:

```python
STYLES = {
    'backtrace': Fore.YELLOW + '{0}',
    'error': Fore.RED + Style.BRIGHT + '{0}',
    'line': Fore.RED + Style.BRIGHT + '{0}',
    'module': '{0}',
    'context': Style.BRIGHT + Fore.GREEN + '{0}',
    'call': Fore.YELLOW + ' --> ' + Style.BRIGHT + '{0}',
}
```

Where:

* `backtrace` is the main traceback message.
* `error` is the error message presenting the exception message and its type.
* `line` is the line number of each entry.
* `module` is the calling module of each entry.
* `context` is the calling function/method of each entry.
* `call` is the called function/method/assignment of each entry.

and the `{0}` format place holder is the actual value of the field.

Sending a partial dictionary containing changes in only some parts of the traceback will have `backtrace` use the defaults for whatever wasn't specified.

You can do all sorts of stuff like removing a certain field by setting the formatting of that field to an empty string; add more verbose identifiers to each field by appending an ID in front of it or just adding paranthese around a field.


## Coloring

Coloring is powered by [colorama](https://github.com/tartley/colorama).


## Testing

To see an example printout:

```shell
$ python test.py
```

```shell
git clone git@github.com:nir0s/backtrace.git
cd backtrace
pip install tox
tox
```

## Contributions..

See [CONTRIBUTIONS](https://github.com/nir0s/backtrace/blob/master/CONTRIBUTING.md)

Pull requests are always welcome..
