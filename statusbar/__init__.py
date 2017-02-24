"""Module for constructing text-based status updates."""

import shutil
import itertools
import termcolor
from math import log10, ceil


class _ProgressChunk:
    def __init__(self, count, symbol, color, on_color, attrs):
        self.count = count
        self.symbol = symbol
        self.color = color
        self.on_color = on_color
        self.attrs = attrs

    def format_chunk(self, width):
        return termcolor.colored(
            self.symbol * width,
            self.color,
            self.on_color,
            self.attrs
        )

    def format_chunk_summary(self):
        return termcolor.colored(
            "{count}".format(count=self.count),
            self.color,
            None,
            self.attrs
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
                     color=None, on_color=None, attrs=None):
        """Add a section of progress to the progressbar.

        The progress is captured by "count" and displayed as a fraction
        of the statusbar width proportional to this count over the total
        progress displayed. The progress will be displayed using the "symbol"
        character and the foreground and background colours and display style
        determined by the the "color", "on_color" and "attrs" parameters.
        These parameters work as the termcolor.colored function.
        """
        chunk = _ProgressChunk(count, symbol, color, on_color, attrs)
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

        # assert sum(chunk_widths) == width
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

    def summary_width(self):
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
                 progress_sep_start='[', progress_sep_end=']', fill_char='.'):
        """Construct a status bar."""
        self.label = label
        self.fill_char = fill_char
        self._progress = ProgressBar(progress_sep_start, progress_sep_end)

    def set_progress_brackets(self, start, end):
        """Define which braces should be used around the progress bar."""
        self._progress.set_progress_brackets(start, end)

    def add_progress(self, count, symbol='#',
                     color=None, on_color=None, attrs=None):
        """Add a section of progress to the progressbar.

        The progress is captured by "count" and displayed as a fraction
        of the statusbar width proportional to this count over the total
        progress displayed. The progress will be displayed using the "symbol"
        character and the foreground and background colours and display style
        determined by the the "fg", "bg" and "style" parameters. For these,
        use the colorama package to set up the formatting.
        """
        self._progress.add_progress(count, symbol, color, on_color, attrs)

    def summary_width(self):
        """Get the minimum width the progress summary field will use."""
        return self._progress.summary_width()

    def label_width(self):
        """Get the minimum width the progress label field will use."""
        return len(self.label)

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
            summary_width = self.summary_width()
        if progress_width is None:
            progress_width = width - label_width - summary_width - 2

        if len(self.label) > label_width:
            # FIXME: This actually *will* break if we ever have fewer than
            # three characters assigned to format the label, but that would
            # be an extreme situation so I won't fix it just yet.
            label = self.label[:label_width - 3] + "..."
        else:
            label_format = "{{label:{fill_char}<{width}}}".format(
                width=label_width,
                fill_char=self.fill_char)
            label = label_format.format(label=self.label)

        summary_format = "{{:>{width}}}".format(width=summary_width)
        summary = summary_format.format(self._progress.format_summary())

        progress = self._progress.format_progress(width=progress_width)

        return "{label} {progress} {summary}".format(
            label=label,
            progress=progress,
            summary=summary
        )


class StatusTable:
    """Several lines of status bars with the three fields aligned."""

    def __init__(self, progress_sep_start='[', progress_sep_end=']'):
        """Create a status table."""
        self._lines = []
        self._sep_start = progress_sep_start
        self._sep_end = progress_sep_end

    def add_status_line(self, label):
        """Add a status bar line to the table.

        This function returns the status bar and it can be modified
        from this return value.
        """
        status_line = StatusBar(label, self._sep_start, self._sep_end)
        self._lines.append(status_line)
        return status_line

    def summary_width(self):
        """Compute the minimum size needed for the summary field."""
        return max(
            sb.summary_width() for sb in self._lines
        )

    def label_width(self):
        """Compute the minimum size needed for the label field.

        This is the minimum size needed if all labels are shown in full.
        If there is not room on a line to shown them in full they will
        be truncated."""
        return max(
            sb.label_width() for sb in self._lines
        )

    def calculate_field_widths(self, width=None,
                               min_label_width=10,
                               min_progress_width=10):
        """Calculate how wide each field should be so we can align them.

        We always find room for the summaries since these are short and
        packed with information. If possible, we will also find room for
        labels, but if this would make the progress bar width shorter than
        the specified minium then we will shorten the labels, though never
        below the minium there. If this mean we have bars that are too wide
        for the terminal, then your terminal needs to be wider.
        """
        if width is None:  # pragma: no cover
            width = shutil.get_terminal_size()[0]

        summary_width = self.summary_width()
        label_width = self.label_width()
        remaining = width - summary_width - label_width - 2

        if remaining >= min_progress_width:
            progress_width = remaining
        else:
            progress_width = min_progress_width
            remaining = width - summary_width - progress_width - 2
            if remaining >= min_label_width:
                label_width = remaining
            else:
                label_width = min_label_width

        return (label_width, progress_width, summary_width)

    def format_table(self, width=None,
                     min_label_width=10, min_progress_width=10):
        """Format the entire table of progress bars.

        The function first computes the widths of the fields so they can be
        aligned across lines and then returns formatted lines as a list of
        strings.
        """
        # handle the special case of an empty table.
        if len(self._lines) == 0:
            return []

        if width is None:  # pragma: no cover
            width = shutil.get_terminal_size()[0]

        labelw, progw, summaryw = self.calculate_field_widths(
            width=width,
            min_label_width=min_label_width,
            min_progress_width=min_progress_width
        )
        output = [
            sb.format_status(
                label_width=labelw,
                progress_width=progw,
                summary_width=summaryw
            )
            for sb in self._lines
        ]

        return output
