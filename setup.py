
# -*- coding: utf-8 -*-
"""
This module contains the tool of sample
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1dev'

long_description = (
    read('README.rst')
    )

setup(name='lisp',
      version=version,
      description="lisp -- a code kata with the objective to implement a lisp",
      long_description=long_description,
      classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='',
      author='Stefan Elethofer',
      author_email='stefan.eletzhofer@nexiles.com',
      url='https://github.com/seletz/lisp.git',
      license='public domain',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      #namespace_packages=['lisp'],
      include_package_data=True,
      zip_safe=False,
      setup_requires=['nose>=1.0'],
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
     entry_points={
          'console_scripts': [
              'lisp = lisp.lisp:main',
              ]
          }
      )

