#!/bin/bash

python3 setup.py sdist
python3 -m pip install dist/defi-value-0.0.0.tar.gz
