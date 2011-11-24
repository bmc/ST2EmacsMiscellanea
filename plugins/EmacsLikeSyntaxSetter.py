import sublime, sublime_plugin
import re
import os

EMACS_SYNTAX_MARK_RE = r'-\*-\s*([^-\s]+)\s*-\*-'

class EmacsLikeSyntaxSetter(sublime_plugin.EventListener):
    '''
    This plugin makes Sublime Text 2 mimic Emacs' behavior of setting
    the buffer syntax based on a special "mode line" somewhere in the
    first non-blank line of a buffer. For instance, if file "foo.C"
    would normally be displayed using C syntax rules, but you want to
    force Sublime to use C++ rules, simply include a comment like this
    in the first non-blank line of the file:

        -*- c++ -*-

    The name of the syntax must match a tmLanguage file somewhere
    under your Sublime "Packages" directory. The match is case-insensitive.
    '''
    def __init__(self):
        self._syntax_re = re.compile(EMACS_SYNTAX_MARK_RE)
        # Find all tmLanguage files below the packages path.
        self._syntaxes = {}

        # Construct a regular expression that will take a full path and
        # yank out everything from "Packages/" to the end. This expression
        # will be use to map paths like /path/to/Packages/C/C.tmLanguage
        # to just Packages/C/C.tmLanguage, which is what Sublime wants
        # as a syntax setting.
        sep = r'\\' if os.sep == "\\" else os.sep
        package_pattern = '^.*%s(Packages%s.*)$' % (sep, sep)
        package_re = re.compile(package_pattern)

        # Walk the directory tree.
        for root, dirs, files in os.walk(sublime.packages_path()):
            # Filter out files that don't end in .tmLanguage
            lang_files = [f for f in files if f.endswith('.tmLanguage')]
            # Map to a full path...
            full_paths = [os.path.join(root, l) for l in lang_files]
            # ... and strip off everything prior to "Packages"
            for p in full_paths:
                # The "Emacs" name is something like "C", or "Python"
                emacs_syntax_name = os.path.splitext(os.path.basename(p))[0]
                # The Sublime name is as described above.
                sublime_syntax_name = package_re.search(p).group(1)
                self._syntaxes[emacs_syntax_name.lower()] = sublime_syntax_name


    def on_activated(self, view):
        self._check_syntax(view)
            
    def on_load(self, view):
        self._check_syntax(view)

    def on_post_save(self, view):
        self._check_syntax(view)
    
    def _check_syntax(self, view):
        buffer_syntax_value = self._find_emacs_syntax_value(view)
        if buffer_syntax_value is not None:
            # The buffer has a syntax setting. See if it maps to one of the
            # known ones.
            syntax = self._map_emacs_syntax_value(buffer_syntax_value)
            if syntax is None:
                name = view.name() or view.file_name()
                print('WARNING: Unknown syntax value "%s" in file "%s".' %
                       (buffer_syntax_value, name))
            else:
                # It does. Is it different from the current syntax of the
                # buffer? If so, change the buffer's syntax setting.
                if view.settings().get('syntax') != syntax:
                    view.set_syntax_file(syntax)

    def _find_emacs_syntax_value(self, view):
        # Must be somewhere in the first nonblank line.
        first_nonblank_line = self._first_nonblank_line(view)
        syntax_expression = None
        if first_nonblank_line is not None:
            m = self._syntax_re.search(first_nonblank_line)
            if m is not None:
                syntax_expression = m.group(1)

        return syntax_expression

    def _map_emacs_syntax_value(self, syntax_name):
        return self._syntaxes.get(unicode(syntax_name.lower()), None)

    def _first_nonblank_line(self, view):
        # Find the first non-blank line and return it.
        point = 0
        size = view.size()
        result = None
        while (result is None) and (point < size):
            # Get the region
            region = view.line(point)
            if region is None:
                break

            # Get the line itself.
            line = view.substr(region)
            if len(line.strip()) > 0:
                result = line
            else:
                # Empty. Move past it.
                point = region.b + 1

        return result
