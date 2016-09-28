import unittest
import statusbar


class TestProgressBar(unittest.TestCase):
    """Test of the progressbar part of a status bar."""

    def test_chunk_widths(self):
        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(1, '#')
        breakpoints = pb._get_chunk_sizes(2)
        self.assertListEqual(breakpoints, [1, 1])

        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(2, '#')
        breakpoints = pb._get_chunk_sizes(3)
        self.assertListEqual(breakpoints, [1, 2])

        # squeezing [1,2] into width 2 will give 1 to each since
        # the first breakpoint is at 2/3 which is rounded up.
        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(2, '#')
        breakpoints = pb._get_chunk_sizes(2)
        self.assertListEqual(breakpoints, [1, 1])

        # squeezing [1,3] into width 2 will give (0,1).
        # The first breakpoint is at 1/2 which *should* be rounded up
        # but actually round(0.5) seems to be 0 in Python...
        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(3, '#')
        breakpoints = pb._get_chunk_sizes(2)
        self.assertListEqual(breakpoints, [0, 2])

        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(3, '#')
        breakpoints = pb._get_chunk_sizes(4)
        self.assertListEqual(breakpoints, [1, 3])
