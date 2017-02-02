=========
Statusbar
=========

Python package for displaying status information in command line interfaces.

|ci-status| |coveralls| |codacy| |license| |versions| |status| |pyversions| |downloads|

.. |ci-status| image:: 	https://img.shields.io/travis/mailund/statusbar.svg
    :target: https://travis-ci.org/mailund/statusbar
    :alt: Build status
.. |coveralls| image:: https://img.shields.io/coveralls/mailund/statusbar.svg
    :target: https://coveralls.io/github/mailund/statusbar
    :alt: Coverage
.. |codacy| image:: https://img.shields.io/codacy/grade/b54b5ad32f964b8b9e5390b72c04964c/master.svg
    :target: https://www.codacy.com/app/mailund/statusbar?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mailund/statusbar&amp;utm_campaign=Badge_Grade
    :alt: Codacy code review
.. |license| image:: https://img.shields.io/pypi/l/statusbar.svg
    :target: https://pypi.python.org/pypi/statusbar
    :alt: License

.. |versions| image:: 	https://img.shields.io/pypi/v/statusbar.svg
    :target: https://pypi.python.org/pypi/statusbar
    :alt: Packgage version
.. |status| image:: https://img.shields.io/pypi/status/statusbar.svg
    :target: https://pypi.python.org/pypi/statusbar
    :alt: Package stability
.. |pyversions| image:: 	https://img.shields.io/pypi/pyversions/statusbar.svg
    :target: https://pypi.python.org/pypi/statusbar
    :alt: Python versions supported
.. |downloads| image:: https://img.shields.io/pypi/dm/statusbar.svg
    :target: https://pypi.python.org/pypi/statusbar
    :alt: Monthly PyPI downloads


This package can be used to show status information through one or more lines of formatted status bars where each status bar consist of three components: a label, a progress bar, and a statistics/summary field.

.. code-block:: python

   import statusbar

   bar = statusbar.StatusBar("Test status")
   bar.add_progress(10, "#")
   bar.add_progress(5, ".")
   print(bar.format_status())

   bar = statusbar.StatusBar("Test status")
   bar.set_progress_brackets('','')
   bar.add_progress(10, " ", color="green")
   bar.add_progress(5, " ", color="red")
   print(bar.format_status())

   st = statusbar.StatusTable()
   sb = st.add_status_line("Test")
   sb.add_progress(1, "#")
   sb.add_progress(1, " ")
   sb = st.add_status_line("Testing progress")
   sb.add_progress(10, "#")
   sb.add_progress(5, ".")
   sb.add_progress(10, " ")
   print("\n".join(st.format_table()))

