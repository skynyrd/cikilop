#!/usr/bin/env sh

set -uex

python -m unittest tests/unit_tests/*.py
python -m unittest tests/integration_tests/*.py