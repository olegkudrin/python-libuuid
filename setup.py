#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""C Extension for faster UUID generation using libuuid."""

__version_info__ = (0, 9, 0)
__version__ = ".".join(map(str, __version_info__))
__author__ = "Daniel Lundin"
__contact__ = "dln@eintr.org"
__homepage__ = "http://github.com/dln/python-libuuid/"
__docformat__ = "restructuredtext"

import codecs
import os
from glob import glob

from setuptools import setup
from distutils.core import Extension
from distutils.command.sdist import sdist

extra_setup_args = {}
try:
    from Cython.Build import cythonize
    import Cython.Compiler.Version
    import Cython.Compiler.Main as cython_compiler
    print("building with Cython " + Cython.Compiler.Version.version)
    class Sdist(sdist):
        def __init__(self, *args, **kwargs):
            for src in glob('libuuid/*.pyx'):
                cython_compiler.compile(glob('libuuid/*.pyx'),
                                        cython_compiler.default_options)
            sdist.__init__(self, *args, **kwargs)
    extra_setup_args['cmdclass'] = {'sdist': Sdist}
    source_extension = ".pyx"
except ImportError as e:
    print("building without Cython")
    cythonize = lambda obj: [obj]
    source_extension = ".c"


libuuid_extension = Extension('libuuid._uuid',
                    sources=['libuuid/_uuid' + source_extension],
                    libraries=['uuid'])


long_description = '\n' + codecs.open('README.rst', "r", "utf-8").read()

setup(name = 'python-libuuid',
      version = __version__,
      description = __doc__,
      author = __author__,
      author_email = __contact__,
      license = 'BSD',
      url = __homepage__,
      packages = ['libuuid'],
      package_dir={'libuuid': 'libuuid'},
      ext_modules = cythonize(libuuid_extension),
      zip_safe=False,
      test_suite="nose.collector",
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Programming Language :: Python",
                   "Programming Language :: Cython",
                   "License :: OSI Approved :: BSD License",
                   "Intended Audience :: Developers",
                   "Topic :: Communications",
                   "Topic :: System :: Distributed Computing",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                  ],
      long_description=long_description,
    **extra_setup_args
)
