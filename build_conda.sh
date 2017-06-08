#!/usr/bin/env bash
#
# Builds and uploads conda packages for the current Python version and
# all supported platforms (osx, win, linux).

set -eu
set -o pipefail

anaconda -t $ANACONDA_TOKEN upload --user mailund $HOME/miniconda/conda-bld/*/*.tar.bz2
