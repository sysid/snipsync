import os
import re
import textwrap
from collections import defaultdict
from typing import List

from snipsync.text import LineIterator, head_tail


def normalize_file_path(path: str) -> str:
    """Calls normpath and normcase on path"""
    return os.path.normcase(os.path.normpath(path))


def handle_extends(tail, line_index):
    """Handles an extends line in a snippet."""
    if tail:
        return "extends", ([p.strip() for p in tail.split(",")],)
    else:
        return "error", ("'extends' without file types", line_index)


def handle_action(head, tail, line_index):
    if tail:
        action = tail.strip('"').replace(r"\"", '"').replace(r"\\\\", r"\\")
        return head, (action,)
    else:
        return "error", ("'{}' without specified action".format(head), line_index)


def handle_context(tail, line_index):
    if tail:
        return "context", tail.strip('"').replace(r"\"", '"').replace(r"\\\\", r"\\")
    else:
        return "error", ("'context' without body", line_index)


class UltiSnipsSnippetDefinition:
    """Represents a snippet as parsed from a file."""

    _INDENT = re.compile(r"^[ \t]*")
    _TABS = re.compile(r"^\t*")

    def __init__(
        self,
        priority,
        trigger,
        value,
        description,
        options,
        globals,
        location,
        context,
        actions,
    ):
        self._priority = int(priority)
        self._trigger = trigger
        self._value = value
        self._description = description
        self._opts = options
        self._matched = ""
        self._last_re = None
        self._globals = globals
        self._location = location
        self._context_code = context
        self._context = None
        self._actions = actions or {}

        # Make sure that we actually match our trigger in case we are
        # immediately expanded.
        # self.matches(self._trigger)

    def __repr__(self):
        return "_SnippetDefinition(%r,%s,%s,%s)" % (
            self._priority,
            self._trigger,
            self._description,
            self._opts,
        )

    def _make_debug_exception(self, e, code=""):
        e.snippet_info = textwrap.dedent(
            """
            Defined in: {}
            Trigger: {}
            Description: {}
            Context: {}
            Pre-expand: {}
            Post-expand: {}
        """
        ).format(
            self._location,
            self._trigger,
            self._description,
            self._context_code if self._context_code else "<none>",
            self._actions["pre_expand"] if "pre_expand" in self._actions else "<none>",
            self._actions["post_expand"]
            if "post_expand" in self._actions
            else "<none>",
            code,
        )

        e.snippet_code = code

    def has_option(self, opt):
        """Check if the named option is set."""
        return opt in self._opts

    @property
    def description(self):
        """Descriptive text for this snippet."""
        return ("(%s) %s" % (self._trigger, self._description)).strip()

    @property
    def priority(self):
        """The snippets priority, which defines which snippet will be preferred
        over others with the same trigger."""
        return self._priority

    @property
    def trigger(self):
        """The trigger text for the snippet."""
        return self._trigger

    @property
    def matched(self):
        """The last text that matched this snippet in match() or
        could_match()."""
        return self._matched

    @property
    def location(self):
        """Where this snippet was defined."""
        return self._location

    @property
    def context(self):
        """The matched context."""
        return self._context

    def instantiate(self, snippet_instance, initial_text, indent):
        """Parses the content of this snippet and brings the corresponding text
        objects alive inside of Vim."""
        raise NotImplementedError()


def _handle_snippet_or_global(
    filename, line, lines, python_globals, priority, pre_expand, context
):
    """Parses the snippet that begins at the current line."""
    start_line_index = lines.line_index
    descr = ""
    opts = ""

    # Ensure this is a snippet
    snip = line.split()[0]

    # Get and strip options if they exist
    remain = line[len(snip) :].strip()
    words = remain.split()

    if len(words) > 2:
        # second to last word ends with a quote
        if '"' not in words[-1] and words[-2][-1] == '"':
            opts = words[-1]
            remain = remain[: -len(opts) - 1].rstrip()

    if "e" in opts and not context:
        left = remain[:-1].rfind('"')
        if left != -1 and left != 0:
            context, remain = remain[left:].strip('"'), remain[:left]

    # Get and strip description if it exists
    remain = remain.strip()
    if len(remain.split()) > 1 and remain[-1] == '"':
        left = remain[:-1].rfind('"')
        if left != -1 and left != 0:
            descr, remain = remain[left:], remain[:left]

    # The rest is the trigger
    trig = remain.strip()
    if len(trig.split()) > 1 or "r" in opts:
        if trig[0] != trig[-1]:
            return "error", ("Invalid multiword trigger: '%s'" % trig, lines.line_index)
        trig = trig[1:-1]
    end = "end" + snip
    content = ""

    found_end = False
    for line in lines:
        if line.rstrip() == end:
            content = content[:-1]  # Chomp the last newline
            found_end = True
            break
        content += line

    if not found_end:
        return "error", ("Missing 'endsnippet' for %r" % trig, lines.line_index)

    if snip == "global":
        python_globals[trig].append(content)
    elif snip == "snippet":
        definition = UltiSnipsSnippetDefinition(
            priority,
            trig,
            content,
            descr,
            opts,
            python_globals,
            "%s:%i" % (filename, start_line_index),
            context,
            pre_expand,
        )
        return "snippet", (definition,)
    else:
        return "error", ("Invalid snippet type: '%s'" % snip, lines.line_index)


def _parse_snippets_file(data: List, filename: str):
    """Parse 'data' assuming it is a snippet file.

    Yields events in the file.

    """

    python_globals = defaultdict(list)
    lines = LineIterator(data)
    current_priority = 0
    actions = {}
    context = None
    for line in lines:
        if not line.strip():
            continue

        head, tail = head_tail(line)
        if head in ("snippet", "global"):
            snippet = _handle_snippet_or_global(
                filename,
                line,
                lines,
                python_globals,
                current_priority,
                actions,
                context,
            )

            actions = {}
            context = None
            if snippet is not None:
                yield snippet
        elif head == "extends":
            # yield handle_extends(tail, lines.line_index)
            pass
        elif head == "clearsnippets":
            # yield "clearsnippets", (current_priority, tail.split())
            pass
        elif head == "context":
            # head, context, = handle_context(tail, lines.line_index)
            # if head == "error":
            #     yield (head, tail)
            pass
        elif head == "priority":
            # try:
            #     current_priority = int(tail.split()[0])
            # except (ValueError, IndexError):
            #     yield "error", ("Invalid priority %r" % tail, lines.line_index)
            pass
        elif head in ["pre_expand", "post_expand", "post_jump"]:
            # head, tail = handle_action(head, tail, lines.line_index)
            # if head == "error":
            #     yield (head, tail)
            # else:
            #     (actions[head],) = tail
            pass
        elif head and not head.startswith("#"):
            yield "error", ("Invalid line %r" % line.rstrip(), lines.line_index)


class UltiSnipsFileSource:
    """Manages all snippets definitions found in rtp for ultisnips."""

    # def _get_all_snippet_files_for(self, ft):
    #     return find_all_snippet_files(ft)

    @staticmethod
    def parse_snippet_file(filedata, filename):
        for event, data in _parse_snippets_file(filedata, filename):
            yield event, data
