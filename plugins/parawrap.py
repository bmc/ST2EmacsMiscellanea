import sublime, sublime_plugin
import string
import textwrap
import re
import comment
import paragraph

class WrapParagraphCommand(paragraph.WrapLinesCommand):
    """
    The Sublime "wrap_width" setting controls both on-screen wrapping and
    the column at which the WrapLinesCommand folds lines. Those two
    settings should be different; otherwise, things don't look right
    on the screen. This plugin looks for a "wrap_paragraph" setting and,
    if found, uses that value to override the value of "wrap_width". Then,
    it invokes the stock SublimeText "wrap_lines" command.

    Bind "wrap_paragraph" to a key to use this command.

    See related bug report: http://sublimetext.userecho.com/topic/82731-/
    """
    def run(self, edit, width=0):
        if width == 0 and self.view.settings().get("wrap_paragraph"):
            try:
                width = int(self.view.settings().get("wrap_paragraph"))
            except TypeError:
                pass

        super(WrapParagraphCommand, self).run(edit, width)
