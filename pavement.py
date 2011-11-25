# Run this through paver to build the package.

from paver.easy import *
from paver.setuputils import setup
from zipfile import ZipFile
import os

setup(
    name="Sublime Text 2 Hacks",
    packages=[],
    version="0.1",
    url="https://github.com/bmc/sublime-text-hacks",
    author="Brian Clapper",
    author_email="bmc@clapper.org"
)

@task
def package():
    '''
    Generate the package
    '''
    with ZipFile("sublime-text-2-hacks.sublime-package", 'w') as zip:
        for f in os.listdir('plugins'):
            zip.write(os.path.join('plugins', f), os.path.basename(f))

