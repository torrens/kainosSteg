#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHONPATH="${PYTHONPATH}"
export PYTHONPATH

python3 steg.py data/death_of_a_naturalist.txt data/mandril.jpg