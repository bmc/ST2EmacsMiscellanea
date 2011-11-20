# Some Sublime Text 2 Stuff

## Intro

This repo contains various hacks (keymaps, etc.) for the [Sublime Text 2][]
text editor.

## Warning

I use these files myself, but *caveat user*. If you use them, and they screw you all to hell, it's not my fault.

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
    $ cp Emacsish-keybindings.sublime-keymap ~/.config/sublime-text-2/Packages/User/Default\ \(Linux\).sublime-keymap

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
* *ctrl-q* maps to `wrap_paragraph` (see the `parawrap` plugin in this repo),
  for consistency with TextMate key bindings. *Alt-q* also maps to
  `wrap_paragraph`.
* Because I rebound *Ctrl-Q*, these bindings map *Ctrl-Alt-q* to `exit`.

#### Unexpected Oddities

With these bindings in place, the Sublime Text 2 menus may not be correct. For
instance, the file menu will still show the standard Sublime Text 2 bindings
for *Open File*, *New File* and *Save File*.

## Plugins

### `parawrap.py`

The stock Sublime Text 2 `wrap_width` setting controls both on-screen wrapping
and the column at which the `wrap_lines` command folds lines. Those two
settings should be different; otherwise, things don't look right on the screen.
`parawrap.py` contains a wrapper command called `wrap_paragraph` that looks for
a `wrap_paragraph` setting. If that setting is found, its (integer) value is
used to override `wrap_width`. Then, the `wrap_paragraph` command invokes the
stock `wrap_lines` command to wrap the paragraph.

See related bug report <http://sublimetext.userecho.com/topic/82731-/>

#### Installation

Copy `paragraph.py` to your Sublime `Packages/User` directory.

#### Settings

Sample settings:

    {
        // On screen, words wrap at 80.
        "wrap_width": 80,

        // When wrap_paragraph is invoke, words wrap at 79.
        "wrap_paragraph": 79,

        "rulers": [80]
    }

#### Key bindings

Bind `wrap_paragraph` to a key:

    { "keys": ["alt+q"], "command": "wrap_paragraph"},
