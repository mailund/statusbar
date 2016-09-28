"""
Module for constructing text-based status updates.
"""
import colorama
import itertools

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
        pass


class ProgressBar:
    """Class responsible for showing progress of a task."""

    def __init__(self):
        self._progress_chunks = []

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
        """Format the progress bar to fit into "width" characters."""
        pass
