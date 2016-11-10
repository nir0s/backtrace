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

backtrace also allows to choose the formatting for each part of the traceback; show the traceback entries in reversed order, and more..

Example:

![](https://github.com/nir0s/backtrace/raw/master/img/main.png)

NOTE: Windows support coming soon!


## Alternatives

* [colored_traceback](https://github.com/staticshock/colored-traceback.py) provides a way to color your tracebacks to make them more readable. It's a nice little tool but lacks actually re-formatting the traceback which is what the biggest problem is from my POV.
* Um.. your own implementation? There's really a reason for me doing this. I do have a life you know (well.. I try anyway).


## Installation

backtrace supports Linux and OSX on Python 2.6, 2.7 and 3.4+

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
    line_format=None,
    file_format=None,
    context_format=None,
    call_format=None)

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

All `*_format` arguments allow for passing different formats for the different parts of each traceback entry and so overriding the defaults. This API is not currently well documented and might be expanded in the future.


## Coloring

Coloring is powered by [colorama](https://github.com/tartley/colorama).

I chose colors that made sense to me. At some point, i'll expose a nicer way of configuring those (for now just use the `*_format` arguments).


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
