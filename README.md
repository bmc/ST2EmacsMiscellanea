# Some Sublime Text 2 Stuff

## Intro

This repo contains various hacks (keymaps, etc.) for the [Sublime Text 2][]
text editor.

## Warning

I use these files myself, but *caveat user*. If you use them, and they screw you all to hell, it's not my fault.

## Emacs-ish Keybindings

The file `Emacsish-keybindings.sublime-keymap` provides various Emacs-like key
bindings for Sublime Text 2. To install these bindings as your default key
bindings, check out this repository and copy the file to the appropriate
directory for your platform, as shown below:

* Linux: `~/.config/sublime-text-2/Packages/User/Default (Linux).sublime-keymap`
* Mac: `/Users/bmc/Library/Application Support/Sublime Text 2/Packages/User`
* Windows: `C:\Users\username\AppData\Roaming\Sublime Text 2\Packages\User\Default (Windows).sublime-keymap` 
  (**NOTE**: That's the path on *my* Windows 7 machine, with `username` 
  replaced by my user name, and using the non-portable version of 
  Sublime Text 2. YMMV.)

For instance, on Linux:

    $ git clone https://github.com/bmc/sublime-text-hacks
    $ cd sublime-text-hacks
    $ cp Emacsish-keybindings.sublime-keymap ~/.config/sublime-text-2/Packages/User/Default\ \(Linux\).sublime-keymap

[Sublime Text 2]: http://www.sublimetext.com/2