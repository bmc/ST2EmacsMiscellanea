# Some Sublime Text 2 Stuff

## Intro

This repo contains various hacks (keymaps, plugins, etc.) for the
[Sublime Text 2][] text editor.

[Sublime Text 2]: http://www.sublimetext.com/2

## Warning

I use these files myself, but *caveat user*. If you use them, and they screw you all to hell, it's not my fault.

## Plugins

### Paragraph Wrapping

The stock Sublime Text 2 `wrap_width` setting controls both on-screen wrapping
and the column at which the `wrap_lines` command folds lines. Those two
settings should be different; otherwise, paragraphs can wrap strangely on the
screen. `parawrap.py` contains a wrapper command called `wrap_paragraph` that
looks for a `wrap_paragraph` setting. If that setting is found, its (integer)
value is used to override `wrap_width`. Then, the `wrap_paragraph` command
invokes the stock `wrap_lines` command to wrap the paragraph.

See related bug report <http://sublimetext.userecho.com/topic/82731-/>

See below for installation instructions.

#### Settings

Sample settings:

    {
        // On screen, words wrap at 80.
        "wrap_width": 80,

        // When wrap_paragraph is invoked, words wrap at 79.
        "wrap_paragraph": 79,

        "rulers": [80]
    }

#### Key bindings

Bind `wrap_paragraph` to a key:

    { "keys": ["alt+q"], "command": "wrap_paragraph"},

### Fixup Whitespace

Emacs has a function called `fixup-whitespace`, documented as:

> This function replaces all the horizontal whitespace surrounding point with
> either one space or no space, according to the context. It returns nil.
>
> At the beginning or end of a line, the appropriate amount of space is none.
> Before a character with close parenthesis syntax, or after a character with
> open parenthesis or expression-prefix syntax, no space is also appropriate.
> Otherwise, one space is appropriate.

(See the [Emacs fixup-whitespace command][] for details.)

This repo provides a plugin, in `plugsin/FixupWhitespace.py` that emulates the
Emacs `fixup-whitespace` command. By default, my key bindings (above) map
the function to *Alt-Space*.

See below for installation instructions.

[Emacs fixup-whitespace command]: http://www.gnu.org/s/emacs/manual/html_node/elisp/User_002dLevel-Deletion.html#index-fixup_002dwhitespace-2569

### Emacs-like Syntax Setter

[GNU Emacs][] has a useful feature that allows an individual file to override
the default Emacs mode (and, hence, the associated language syntax and
colorization) by using a special magic string somewhere in the first non-blank
line of the file. (For documentation on this Emacs feature, see the Emacs
[Choosing Modes][] documentation node.)

[GNU Emacs]: http://www.gnu.org/s/emacs/
[Choosing Modes]: http://www.gnu.org/software/emacs/manual/html_node/emacs/Choosing-Modes.html>

The `EmacsLikeSyntaxSetter.py` plugin, in this repository, provides a similar
capability for Sublime Text 2.

For instance, if file `foo.C` would normally be displayed using C syntax rules,
but you want to force Sublime Text 2 to use C++ rules, simply include a comment
like this in the first non-blank line of the file:

    //              -*- c++ -*-

Notes:

* The spaces between the `-*-` markers are optional, and any number of them is
  permitted (including none).
* The syntax name must match the name of a `.tmLanguage` file somewhere
  underneath your Sublime Text 2 `Packages` directory. The name is matched
  in a case-blind manner; thus, "Scala" and "scala" mean the same thing.
  
Thus, the following lines all set the buffer syntax to "Python":

    #  -*-python-*-
    #                    -*-        Python-*-
    #         -*- PyThOn -*-
    # -*- Python -*-

The plugin scans the buffer for a syntax-setting line under three
circumstances:

1. When you first load a file into a new view (buffer).
2. Right after you save a buffer.
3. When the buffer is activated (i.e., given keyboard focus).

If you're editing a file, and you change the syntax line, you'll either
have to save the buffer, or focus out and focus back on it, to force the
new syntax setting to take effect.

If the plugin fails to honor your syntax setting, see the Python console
(normally accessible via *Ctrl-`*). There may be a warning that's helpful.

See below for installation instructions.

### Plugin Installation

There are several ways to install these plugins.

NOTE: The plugins do _not_ install any key bindings by default. If you want to
use my key bindings, see below.

#### Via Package Control

If you're using Will Bond's [Package Control][] (and you should be):

First add this repository to your Package Control repo list. (This step won't
be necessary once the repository is listed in the master Package Control
repository list, which should be soon):

Go to the *Preferences > Packages Settings > Package Control > Settings - User*
menu. That will bring up `Package Control.sublime-settings` in a buffer. In the resulting buffer, make sure "repositories" contains
"https://github.com/bmc/sublime-text-hacks". For instance, my file looks
like this:

    {
      "auto_upgrade_last_run": 1322234232,
      "repositories":
      [
        "https://github.com/bmc/sublime-text-hacks"
      ]
    }

Then, pull up *Preferences > Package Control*, select
*Package Control: Install Package*, and search for "hacks". It should point
to this package, which you can then install.

To upgrade the package, just use the Package Control package upgrade 
capability.

[Package Control]: http://wbond.net/sublime_packages/package_control

#### Manually


Go to your Sublime Text 2 `Packages` directory and clone the repository.
For instance, on Linux:

    $ cd ~/.config/sublime-text-2/Packages
    $ git clone https://github.com/bmc/sublime-text-hacks

On Mac OS X:

    $ cd "$HOME/Library/Application Support/Sublime Text 2/Packages"
    $ git clone https://github.com/bmc/sublime-text-hacks

It might be necessary to restart the editor.

To upgrade, just do a `git pull` within that directory.

## Key Bindings

### Emacs-ish Key Bindings

The file `Emacsish-keybindings.sublime-keymap` provides various Emacs-like key
bindings for Sublime Text 2.

#### Prerequisites

By default, the key bindings use Stian Grytøyr's Emacs-style *kill ring*
implementation, available at <https://github.com/stiang/EmacsKillRing>. If you
prefer the more standard, Windows-like cut-and-paste semantics, see the
`Emacsish-keybindings.sublime-keymap` file. You can comment out the kill ring
mappings and uncomment the cut-and-paste mappings, instead.

#### Installation

To install these bindings as your default key bindings, check out this
repository and copy the file to the appropriate directory for your platform, as
shown below:

* Linux: `~/.config/sublime-text-2/Packages/User/Default (Linux).sublime-keymap`
* Mac: `/Users/bmc/Library/Application Support/Sublime Text 2/Packages/User\Default (OSX).sublime-keymap`
* Windows: `C:\Users\username\AppData\Roaming\Sublime Text 2\Packages\User\Default (Windows).sublime-keymap` 
  (**NOTE**: That's the path on *my* Windows 7 machine, with `username` 
  replaced by my user name, and using the non-portable version of 
  Sublime Text 2. YMMV.)

For instance, on Linux:

    $ git clone https://github.com/bmc/sublime-text-hacks
    $ cd sublime-text-hacks
    $ cp keymaps/Emacsish-keybindings.sublime-keymap ~/.config/sublime-text-2/Packages/User

#### Non-Standard Emacs Mappings

* *Incremental Search* (not "regular search") is bound to *Ctrl-s*.
* *Ctrl-r* is bound to *Reverse Incremental Search*.
* *Alt-r* (*Command-r* on the Mac) is bound to *Search and Replace*.
* *Alt-s* (*Command-s* on the Mac) is bound to *Save*, as well, for consistency
  with TextMate and other Mac applications. (You can comment this out, or 
  rebind it.)
* *Ctrl-/* is bound to *Undo*, mostly because that's what I'm used to using.
* *Alt-z* (*Command-z* on the Mac) is also bound to *Undo*, for consistency
  with TextMate and other Mac applications.
* *Ctrl-Alt-n* is bound to *New File*.
* *Ctrl-Alt-o* is bound to *Open File*, as is the more standard Emacs
  *Ctrl-x Ctrl-f* key sequence.
* Pressing *Ctrl-s* repeatedly does not continue the incremental search.
  Use F3 for that. There may be a way to have *Ctrl-s* do what I want,
  perhaps by using contexts. I'm not sure how to do that yet.
* *Ctrl-q* maps to `wrap_paragraph` (see the `parawrap` plugin in this repo),
  for consistency with TextMate key bindings. *Alt-q* also maps to
  `wrap_paragraph`.
* Because I rebound *Ctrl-Q*, these bindings map *Ctrl-Alt-q* to `exit`.
* *Alt-Space* is bound to `fixup_whitespace`, which is implemented via my
  Fixup Whitespace plugin, below.

#### Unexpected Oddities

With these bindings in place, the Sublime Text 2 menus may not be correct. For
instance, the file menu will still show the standard Sublime Text 2 bindings
for *Open File*, *New File* and *Save File*.

## Other Repos

* [Eric Hamiter](https://github.com/ehamiter) has a repository of
  Sublime Text 2 plugins: <https://github.com/ehamiter/Sublime-Text-2-Plugins>
* [Jim Powers](https://github.com/corruptmemory) also has a repository with
  some Sublime hacks: <https://github.com/corruptmemory/sublime-text>
