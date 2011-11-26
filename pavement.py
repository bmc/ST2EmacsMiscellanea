# Run through "paver" (http://paver.github.com/paver/).

from paver.easy import *
from paver.setuputils import setup
import json
import platform
import os
import shutil

PLATFORM_MAP = {
    "Darwin" : "OSX",
    "Windows": "Windows",
    "Linux"  : "Linux"
}

metadata = json.loads(''.join(open("package-metadata.json").readlines()))
setup(
    name         = "sublime-text-hacks",
    version      = metadata['version'],
    url          = 'https://github.com/bmc/sublime-text-hacks',
    author       = 'Brian Clapper',
    author_email = 'bmc@clapper.org'
)

@task
@needs('installmousebindings', 'installkeybindings')
def installbindings():
    """Install the key and mouse bindings"""
    pass

@task
def installkeybindings():
    """Install the key bindings"""
    sublime_platform = _get_sublime_platform()
    base = _get_sublime_dir(sublime_platform)
    target_dir = os.path.join(base, 'Packages', 'User')

    keybindings_target = os.path.join(
        target_dir, "Default (%s).sublime-keymap" % sublime_platform
    )

    rm_f(keybindings_target)
    cp("bindings/Emacsish-keybindings.sublime-keymap", keybindings_target)

@task
def installmousebindings():
    """Install the mouse bindings"""
    sublime_platform = _get_sublime_platform()
    base = _get_sublime_dir(sublime_platform)
    target_dir = os.path.join(base, 'Packages', 'User')

    mousebindings_target = os.path.join(
        target_dir, "Default (%s).sublime-mousemap" % sublime_platform
    )

    rm_f(mousebindings_target)
    cp("bindings/mousebindings.sublime-mousemap", mousebindings_target)

def cp(source, dest):
    if not os.path.exists(source):
        raise Exception('Source file "%s" does not exist.' % source)

    print('+ cp %s "%s"' % (source, dest))
    shutil.copy(source, dest)

def rm_f(path):
    print('+ rm -f %s' % path)
    os.unlink(path)

def _get_sublime_dir(sublime_platform):
    if sublime_platform == "Darwin":
        base = os.path.expanduser("~/Library/Application Support/Sublime Text 2")
    elif sublime_platform == "Windows":
        user = os.environ.get("USERNAME")
        base = r'C:\Users\%s\AppData\Roaming\Sublime Text 2' % user
    else: # Linux
        base = os.path.expanduser("~/.config/sublime-text-2")
    return base

def _get_sublime_platform():
    sublime_platform = PLATFORM_MAP.get(platform.system(), None)
    if sublime_platform is None:
        raise Exception("Unknown platform: %s" % platform.system())
    return sublime_platform