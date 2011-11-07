# Some Sublime Text 2 Stuff

## Intro

This repo contains various hacks (keymaps, etc.) for the [Sublime Text 2][]
text editor.

## Warning

I use these files myself, but *caveat user*. If you use them, and they screw you all to hell, it's not my fault.

## Emacs-ish Keybindings

The file `Emacsish-keybindings.sublime-keymap` provides various Emacs-like key
bindings for Sublime Text 2.

### Prerequisites

By default, the key bindings use Stian Grytøyr's Emacs-style *kill ring*
implementation, available at <https://github.com/stiang/EmacsKillRing>. If you
prefer the more standard, Windows-like cut-and-paste semantics, see the
`Emacsish-keybindings.sublime-keymap` file. You can comment out the kill ring
mappings and uncomment the cut-and-paste mappings, instead.

### Installation

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

### Non-Standard Emacs Mappings

* *Incremental Search* is bound to *Ctrl-s*, not "regular" search.
* *Ctrl-r* is bound to *Reverse Incremental Search*.
* *Alt-R* (*Command-r* on the Mac) is bound to *Search and Replace*.
* *Alt-s* (*Command-s* on the Mac) is bound to *Save*, as well, for consistency
  with TextMate and other Mac applications. (You can comment this out, or 
  rebind it.)
* *Ctrl-/* is bound to *Undo*, mostly because that's what I'm used to using.
* *Alt-z (*Command-z* on the Mac) is also bound to *Undo*, for consistency with
  TextMate and other Mac applications.
* *Ctrl-Alt-n* is bound to *New File*.
* *Ctrl-Alt-o* is bound to *Open File*, as is the more standard Emacs
  *Ctrl-x Ctrl-f* key sequence.
* Pressing *Ctrl-s* repeatedly does not continue the incremental search.
  Use F3 for that. I'm sure there's a way to have *Ctrl-Alt-S* do what I want,
  perhaps by using contexts. I'm not sure how to do that yet.

### Unexpected Oddities

With these bindings in place, the Sublime Text 2 menus may not be correct. For
instance, the file menu will still show the standard Sublime Text 2 bindings
for *Open File*, *New File* and *Save File*.

[Sublime Text 2]: http://www.sublimetext.com/2