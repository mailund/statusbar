import unittest
import colorama
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

    def test_progress_formatting(self):
        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(1, '#')
        progress = pb.format_progress(4)
        self.assertEqual(progress, "[.#]")

        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(2, '#')
        progress = pb.format_progress(5)
        self.assertEqual(progress, "[.##]")

        # Adding a forground colour makes each segment ten characters
        # longer; five characters are used for setting the color and another
        # five for resetting it again. These are not shown, so the width
        # doesn't take this into account.
        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.', fg=colorama.Fore.GREEN)
        pb.add_progress(2, '#', fg=colorama.Fore.RED)
        progress = pb.format_progress(5)
        self.assertEqual(progress[0], "[")
        self.assertEqual(progress[1:6], colorama.Fore.GREEN)
        self.assertEqual(progress[6], ".")
        self.assertEqual(progress[7:12], colorama.Fore.RESET)
        self.assertEqual(progress[12:17], colorama.Fore.RED)
        self.assertEqual(progress[17:19], "##")
        self.assertEqual(progress[19:24], colorama.Fore.RESET)
        self.assertEqual(progress[24], "]")
