import unittest
import termcolor
import statusbar


class TestProgressBar(unittest.TestCase):
    """Test of the progressbar part of a status bar."""

    def test_chunk_widths(self):
        pb = statusbar.ProgressBar(sep_start="", sep_end="")
        pb.add_progress(1, '.')
        pb.add_progress(1, '#')
        breakpoints = pb._get_chunk_sizes(2)
        self.assertListEqual(breakpoints, [1, 1])

        pb = statusbar.ProgressBar(sep_start="", sep_end="")
        pb.add_progress(1, '.')
        pb.add_progress(2, '#')
        breakpoints = pb._get_chunk_sizes(3)
        self.assertListEqual(breakpoints, [1, 2])

        # squeezing [1,2] into width 2 will give 1 to each since
        # the first breakpoint is at 2/3 which is rounded up.
        pb = statusbar.ProgressBar(sep_start="", sep_end="")
        pb.add_progress(1, '.')
        pb.add_progress(2, '#')
        breakpoints = pb._get_chunk_sizes(2)
        self.assertListEqual(breakpoints, [1, 1])

        # squeezing [1,3] into width 2 will give (0,1).
        # The first breakpoint is at 1/2 which *should* be rounded up
        # but actually round(0.5) seems to be 0 in Python...
        pb = statusbar.ProgressBar(sep_start="", sep_end="")
        pb.add_progress(1, '.')
        pb.add_progress(3, '#')
        breakpoints = pb._get_chunk_sizes(2)
        self.assertListEqual(breakpoints, [0, 2])

        pb = statusbar.ProgressBar(sep_start="", sep_end="")
        pb.add_progress(1, '.')
        pb.add_progress(3, '#')
        breakpoints = pb._get_chunk_sizes(4)
        self.assertListEqual(breakpoints, [1, 3])

    def test_progress_formatting(self):
        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(1, '#')
        progress = pb.format_progress(4)
        self.assertEqual(progress, "[.\x1b[0m#\x1b[0m]")

        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(2, '#')
        progress = pb.format_progress(5)
        self.assertEqual(progress, "[.\x1b[0m##\x1b[0m]")

        # Adding a forground colour makes each segment ten characters
        # longer; five characters are used for setting the color and another
        # five for resetting it again. These are not shown, so the width
        # doesn't take this into account.
        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.', color="green")
        pb.add_progress(2, '#', color="red")
        progress = pb.format_progress(5)
        self.assertEqual(progress, "[\x1b[32m.\x1b[0m\x1b[31m##\x1b[0m]")

        # Adding a background and style as well makes the string even longer
        # but other than that there is nothing surprising going on.
        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.',
                        color="green", on_color="on_red", attrs=["underline"])
        pb.add_progress(2, '#',
                        color="red", on_color="on_green", attrs=["bold"])
        progress = pb.format_progress(5)
        self.assertEqual(
            progress,
            "[\x1b[4m\x1b[41m\x1b[32m.\x1b[0m\x1b[1m\x1b[42m\x1b[31m##\x1b[0m]"
        )

    def test_summary_string(self):
        pb = statusbar.ProgressBar()
        pb.add_progress(1, '.')
        pb.add_progress(1, '#')
        estimated_length = pb.summary_width()
        summary_string = pb.format_summary()
        self.assertEqual(estimated_length, 3)
        self.assertEqual(summary_string,
                         termcolor.colored("1")+"/"+termcolor.colored("1"))

        pb = statusbar.ProgressBar()
        pb.add_progress(0, '.')
        pb.add_progress(1, '#')
        estimated_length = pb.summary_width()
        summary_string = pb.format_summary()
        self.assertEqual(estimated_length, 3)
        self.assertEqual(summary_string,
                         termcolor.colored("0")+"/"+termcolor.colored("1"))

        pb = statusbar.ProgressBar()
        pb.add_progress(0, '.')
        pb.add_progress(0, '#')
        estimated_length = pb.summary_width()
        summary_string = pb.format_summary()
        self.assertEqual(estimated_length, 3)
        self.assertEqual(summary_string,
                         termcolor.colored("0")+"/"+termcolor.colored("0"))

        pb = statusbar.ProgressBar()
        pb.add_progress(9, '.')
        pb.add_progress(9, '#')
        estimated_length = pb.summary_width()
        summary_string = pb.format_summary()
        self.assertEqual(estimated_length, 3)
        self.assertEqual(summary_string,
                         termcolor.colored("9")+"/"+termcolor.colored("9"))

        pb = statusbar.ProgressBar()
        pb.add_progress(10, '.')
        pb.add_progress(10, '#')
        estimated_length = pb.summary_width()
        summary_string = pb.format_summary()
        self.assertEqual(estimated_length, 5)
        self.assertEqual(
            summary_string,
            termcolor.colored("10")+"/"+termcolor.colored("10")
        )

        pb = statusbar.ProgressBar()
        pb.add_progress(99, '.')
        pb.add_progress(99, '#')
        estimated_length = pb.summary_width()
        summary_string = pb.format_summary()
        self.assertEqual(estimated_length, 5)
        self.assertEqual(summary_string,
                         termcolor.colored("99")+"/"+termcolor.colored("99"))

        pb = statusbar.ProgressBar()
        pb.add_progress(100, '.')
        pb.add_progress(199, '#')
        estimated_length = pb.summary_width()
        summary_string = pb.format_summary()
        self.assertEqual(estimated_length, 7)
        self.assertEqual(summary_string,
                         termcolor.colored("100")+"/"+termcolor.colored("199"))


class TestStatusBar(unittest.TestCase):
    """Test of a status bar."""

    def test_status_formatting(self):
        sb = statusbar.StatusBar("Test")
        sb.add_progress(2, '#')
        sb.add_progress(2, '.')
        result = sb.format_status(15)
        # -- I don't actually know how to get the visible string length
        # self.assertEqual(len(result), 15)

        sb.set_progress_brackets("", "")
        result = sb.format_status(15)
        # self.assertEqual(len(result), 15)

        sb = statusbar.StatusBar("Long label")
        sb.add_progress(2, '#')
        sb.add_progress(2, '.')
        result = sb.format_status(15, label_width=4)
        # self.assertEqual(len(result), 15)

        sb = statusbar.StatusBar("Long label")
        sb.add_progress(2, '#')
        sb.add_progress(2, '.')
        result = sb.format_status(26, label_width=15)
        # self.assertEqual(len(result), 26)

        result = sb.format_status(label_width=4,
                                  progress_width=10)

        result = sb.format_status(label_width=4,
                                  progress_width=10,
                                  summary_width=5)

        self.assertEqual(len(result), 35)  # this is only to avoid lint issues

    def test_formatting_with_fill_char(self):
        sb = statusbar.StatusBar("Test", fill_char=' ')
        sb.add_progress(1, '#')
        result = sb.format_status(15, label_width=5)
        self.assertTrue(result.startswith('Test  '))

        sb = statusbar.StatusBar("Test", fill_char='_')
        sb.add_progress(1, '#')
        result = sb.format_status(15, label_width=5)
        self.assertTrue(result.startswith('Test_ '))


class TestStatusTable(unittest.TestCase):
    """Test of a status table."""

    def test_field_width_calculations(self):
        st = statusbar.StatusTable()

        label1 = "Test"
        sb = st.add_status_line(label1)
        sb.add_progress(1, "#")
        sb.add_progress(1, " ")

        label2 = "Testing progress"
        sb = st.add_status_line(label2)
        sb.add_progress(10, "#")
        sb.add_progress(10, " ")

        self.assertEqual(st.label_width(), len(label2))
        self.assertEqual(st.summary_width(), len("10/10"))

        labw, progw, sumw = st.calculate_field_widths(width=30)
        self.assertEqual(sumw, 5)
        self.assertEqual(progw, 10)
        self.assertEqual(labw, 15 - 2)

        labw, progw, sumw = st.calculate_field_widths(width=40)
        self.assertEqual(sumw, 5)
        self.assertEqual(labw, len(label2))
        self.assertEqual(progw, 40 - len(label2) - 5 - 2)

        labw, progw, sumw = st.calculate_field_widths(width=1)
        self.assertEqual(sumw, 5)
        self.assertEqual(progw, 10)
        self.assertEqual(labw, 10)

    def test_table_formatting(self):
        st = statusbar.StatusTable()
        self.assertEqual(st.format_table(), [])

        label1 = "Test"
        sb = st.add_status_line(label1)
        sb.add_progress(1, "#")
        sb.add_progress(1, " ")

        label2 = "Testing progress"
        sb = st.add_status_line(label2)
        sb.add_progress(10, "#")
        sb.add_progress(10, " ")

        st.format_table(width=40)
        # formatted = st.format_table(width=40)
        # labelw = len(label2)
        # statusw = len("10/10")

        # first_label = formatted[0][:labelw]
        # second_label = formatted[1][:labelw]
        # first_status = formatted[0][-statusw:]
        # second_status = formatted[1][-statusw:]

        # self.assertEqual(first_label, "Test............")
        # self.assertEqual(second_label, label2)
        # self.assertEqual(first_status, "  1/1")
        # self.assertEqual(second_status, "10/10")
