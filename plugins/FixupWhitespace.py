import sublime, sublime_plugin

class FixupWhitespaceCommand(sublime_plugin.TextCommand):
    '''
    FixupWhitespaceCommand is a Sublime Text 2 plugin command that emulates
    the Emacs (fixup-whitespace) command: It collapses white space behind
    and ahead of the cursor, leaving just one space. For compatibility with
    Emacs, if the cursor is in the first column, this plugin leaves no spaces.
    '''

    def run(self, edit):
        sel = self.view.sel()
        if (sel is None) or (len(sel) == 0):
            return

        # Determine whether there's white space at the cursor.

        cursor_region = sel[0]
        point = cursor_region.begin()
        line = self.view.line(point)
        cur = self.view.substr(point)
        prev = self.view.substr(point - 1) if point > line.begin() else u'\x00'

        if prev.isspace():
            prefix_ws_region = self._handle_prefix_whitespace(point, line)
        else:
            prefix_ws_region = None

        if cur.isspace() and (not self._line_end(cur)):
            suffix_ws_region = self._handle_suffix_whitespace(point, line)
        else:
            suffix_ws_region = None

        # Now do the actual delete, using the Sublime Text standard
        # edit block approach, which allows for undo.
        try:
            edit = self.view.begin_edit()
            if suffix_ws_region is not None:
                self.view.erase(edit, suffix_ws_region)

            if prefix_ws_region is not None:
                self.view.erase(edit, prefix_ws_region)

            # Make sure there's one blank left, unless:
            #
            # a) the next character is not a letter or digit, or
            # b) the previous character is not a letter or digit, or
            # c) we're at the beginning of the line
            point = self.view.sel()[0].begin()
            bol = line.begin()
            if point > bol:
                def letter_or_digit(c):
                    return c.isdigit() or c.isalpha()

                c = self.view.substr(point)
                c_prev = self.view.substr(point - 1)

                if letter_or_digit(c) and letter_or_digit(c_prev):
                    self.view.insert(edit, point, ' ')

        finally:
            self.view.end_edit(edit)
   
    def _handle_prefix_whitespace(self, point, line):
        p = point
        p -= 1
        c = self.view.substr(p)
        bol = line.begin()
        while (p > bol) and c.isspace():
            p -= 1
            c = self.view.substr(p)

        # "point" is now one character behind where we want it to be,
        # unless we're at the beginning of the line.
        if p > bol or (not c.isspace()):
            p += 1

        # Return the region of white space.
        return sublime.Region(p, point)

    def _handle_suffix_whitespace(self, point, line):
        p = point
        c = self.view.substr(p)
        bol = line.begin()
        eol = line.end()
        while (p <= eol) and (c.isspace()) and (not self._line_end(c)):
            p += 1
            c = self.view.substr(p)
        
        # Return the region of white space.
        return sublime.Region(point, p)

    def _line_end(self, c):
        return (c in ["\r", "\n", u'\x00'])