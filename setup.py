import os
import codecs
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='backtrace',
    version="0.2.0",
    url='https://github.com/nir0s/backtrace',
    author='nir0s',
    author_email='nir36g@gmail.com',
    license='LICENSE',
    platforms='All',
    description='Makes tracebacks humanly readable',
    long_description=read('README.rst'),
    py_modules=['backtrace'],
    entry_points={'console_scripts': ['backtrace = backtrace:main']},
    install_requires=[
        "colorama==0.3.7",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
