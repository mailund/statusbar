"""Module for constructing text-based status updates."""

import shutil
import itertools
import colorama
from math import log10, ceil

colorama.init()


class _ProgressChunk:
    def __init__(self, count, symbol, fg, bg, style):
        self.count = count
        self.symbol = symbol
        self.fg = fg
        self.bg = bg
        self.style = style

        if self.fg is None:
            self.fg = ''
            self.fg_reset = ''
        else:
            self.fg_reset = colorama.Fore.RESET

        if self.bg is None:
            self.bg = ''
            self.bg_reset = ''
        else:
            self.bg_reset = colorama.Back.RESET

        if self.style is None:
            self.style = ''
            self.style_reset = ''
        else:
            self.style_reset = colorama.Style.RESET_ALL

    def format_chunk(self, width):
        return "{format_start}{bar}{format_end}".format(
            format_start=self.style + self.bg + self.fg,
            bar=self.symbol * width,
            format_end=self.fg_reset + self.bg_reset + self.style_reset
        )

    def format_chunk_summary(self):
        return "{format_start}{count}{format_end}".format(
            format_start=self.style + self.bg + self.fg,
            count=self.count,
            format_end=self.fg_reset + self.bg_reset + self.style_reset
        )


class ProgressBar:
    """Class responsible for showing progress of a task."""

    def __init__(self, sep_start='[', sep_end=']'):
        """Construct a progress bar."""
        self._progress_chunks = []
        self.sep_start = sep_start
        self.sep_end = sep_end

    def set_progress_brackets(self, start, end):
        """Set brackets to set around a progress bar."""
        self.sep_start = start
        self.sep_end = end

    def add_progress(self, count, symbol='#',
                     fg=None, bg=None, style=None):
        """Add a section of progress to the progressbar.

        The progress is captured by "count" and displayed as a fraction
        of the statusbar width proportional to this count over the total
        progress displayed. The progress will be displayed using the "symbol"
        character and the foreground and background colours and display style
        determined by the the "fg", "bg" and "style" parameters. For these,
        use the colorama package to set up the formatting.
        """
        chunk = _ProgressChunk(count, symbol, fg, bg, style)
        self._progress_chunks.append(chunk)

    def _get_chunk_sizes(self, width):

        # FIXME: using len() here doesn't work with invisible symbols
        # or things like tabs that take up one character but uses more
        # space in the terminal.
        width = width - len(self.sep_start + self.sep_end)

        chunk_counts = [chunk.count for chunk in self._progress_chunks]
        total = sum(chunk_counts)
        chunk_real_widths = [chunk/total*width for chunk in chunk_counts]
        chunk_break_points = \
            [int(round(bp)) for bp in itertools.accumulate(chunk_real_widths)]

        start_points = [0] + chunk_break_points[:-1]
        end_points = chunk_break_points
        chunk_widths = \
            [(end-start) for (start, end) in zip(start_points, end_points)]

        assert sum(chunk_widths) == width
        return chunk_widths

    def format_progress(self, width):
        """Create the formatted string that displays the progress."""
        chunk_widths = self._get_chunk_sizes(width)
        progress_chunks = [chunk.format_chunk(chunk_width)
                           for (chunk, chunk_width)
                           in zip(self._progress_chunks, chunk_widths)]
        return "{sep_start}{progress}{sep_end}".format(
            sep_start=self.sep_start,
            progress="".join(progress_chunks),
            sep_end=self.sep_end
        )

    def summary_length(self):
        """Calculate how long a string is needed to show a summary string.

        This is not simply the length of the formatted summary string
        since that string might contain ANSI codes.
        """
        chunk_counts = [chunk.count for chunk in self._progress_chunks]
        numbers_width = sum(max(1, ceil(log10(count + 1)))
                            for count in chunk_counts)
        separators_with = len(chunk_counts) - 1
        return numbers_width + separators_with

    def format_summary(self):
        """Generate a summary string for the progress bar."""
        chunks = [chunk.format_chunk_summary()
                  for chunk in self._progress_chunks]
        return "/".join(chunks)


class StatusBar:
    """Class for displaying status bars.

    These bars consists of a label, a progress bar, and statistics/summaries
    of the progress.
    """

    def __init__(self, label,
                 progress_sep_start='[', progress_sep_end=']'):
        """Construct a status bar."""
        self.label = label
        self._progress = ProgressBar(progress_sep_start, progress_sep_end)

    def set_progress_brackets(self, start, end):
        """Define which braces should be used around the progress bar."""
        self._progress.set_progress_brackets(start, end)

    def add_progress(self, count, symbol='#',
                     fg=None, bg=None, style=None):
        """Add a section of progress to the progressbar.

        The progress is captured by "count" and displayed as a fraction
        of the statusbar width proportional to this count over the total
        progress displayed. The progress will be displayed using the "symbol"
        character and the foreground and background colours and display style
        determined by the the "fg", "bg" and "style" parameters. For these,
        use the colorama package to set up the formatting.
        """
        self._progress.add_progress(count, symbol, fg, bg, style)

    def format_status(self, width=None,
                      label_width=None,
                      progress_width=None,
                      summary_width=None):
        """Generate the formatted status bar string."""
        if width is None:  # pragma: no cover
            width = shutil.get_terminal_size()[0]

        if label_width is None:
            label_width = len(self.label)
        if summary_width is None:
            summary_width = self._progress.summary_length()
        if progress_width is None:
            progress_width = width - label_width - summary_width - 2

        if len(self.label) > label_width:
            # FIXME: This actually *will* break if we ever have fewer than
            # three characters assigned to format the label, but that would
            # be an extreme situation so I won't fix it just yet.
            label = self.label[:label_width - 3] + "..."
        else:
            label_format = "{{label:.<{width}}}".format(width=label_width)
            label = label_format.format(label=self.label)

        summary_format = "{{:>{width}}}".format(width=summary_width)
        summary = summary_format.format(self._progress.format_summary())

        progress = self._progress.format_progress(width=progress_width)

        return "{label} {progress} {summary}".format(
            label=label,
            progress=progress,
            summary=summary
        )
