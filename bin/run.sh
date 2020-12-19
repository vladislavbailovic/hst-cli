#!/bin/bash

python setup.py sdist && pip install dist/hst-cli-0.0.1.tar.gz && hst
