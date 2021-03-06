#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'uvloop==0.14.0',
    'quart==0.12.0',
    'peewee==3.13.3',
    'passlib==1.7.2',
    ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Harshad Sharma",
    author_email='harshad@sharma.io',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="SqrlWiki is a wiki for personal notes.",
    entry_points={
        'console_scripts': [
            'sqrlwiki=sqrlwiki.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sqrlwiki',
    name='sqrlwiki',
    packages=find_packages(include=['sqrlwiki', 'sqrlwiki.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hiway/sqrlwiki',
    version='0.1.0',
    zip_safe=False,
)
