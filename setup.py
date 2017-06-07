#!/usr/bin/env python
"""Setup logic for pip."""

from setuptools import setup


def get_long_description():
    """Get long description used on PyPI project page."""
    try:
        # Use pandoc to create reStructuredText README if possible
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except:
        return None


setup(
    name='automata-lib-1.0.0-review-and-fix',
    version='1.0.0acue',
    description='Patches foraA Python library for simulating automata and Turing machines',
    long_description=get_long_description(),
    url='https://github.com/ArnoCan/automata-lib-1.0.0-review-and-fix',
    author='Arno-Can Uestuensoez',
    license='MIT',
    keywords='automata turing machine',
    packages=[
        'automata',
        'automata.fa',
        'automata.pda',
        'automata.shared',
        'automata.tm'
    ],
    install_requires=[],
    entry_points={}
)
