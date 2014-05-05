from setuptools import setup, find_packages, Command
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGELOG = open(os.path.join(here, 'CHANGELOG.txt')).read()

version = '0.0.1'

install_requires = [
    'raven',
]

setup(name='raven-shell',
    version=version,
    description="Sentry client for shell scripts.",
    long_description=README + '\n\n' + CHANGELOG,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='sentry raven shell sh bash',
    author='Roberto Abdelkader Mart\xc3\xadnez P\xc3\xa9rez',
    author_email='robertomartinezp@gmail.com',
    url='https://github.com/nilp0inter/raven-shell',
    license='GPLv3',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['raise=ravenshell:raise_']
    },
)
