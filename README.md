# statusbar

Python package for displaying status information in command line interfaces.

[![Build status](https://img.shields.io/travis/mailund/statusbar.svg)](https://travis-ci.org/mailund/statusbar)
[![Coverage Status](https://img.shields.io/coveralls/mailund/statusbar.svg)](https://coveralls.io/github/mailund/statusbar)
[![License](https://img.shields.io/badge/license-GPL%20%28%3E=%203%29-brightgreen.svg?style=flat)](http://www.gnu.org/licenses/gpl-3.0.html)


This package can be used to show status information through one or more lines of formatted status bars where each status bar consist of three components: a label, a progress bar, and a statistics/summary field.

```Python
import colorama
import statusbar

bar = statusbar.StatusBar("Test status")
bar.add_progress(10, "#")
bar.add_progress(5, ".")
print(bar.format_status())

bar = statusbar.StatusBar("Test status")
bar.set_progress_brackets('','')
bar.add_progress(10, " ", bg=colorama.Back.GREEN)
bar.add_progress(5, " ", bg=colorama.Back.RED)
print(bar.format_status())
```
