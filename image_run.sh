#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHONPATH="${PYTHONPATH}"
export PYTHONPATH

python3 image_steg.py data/cheltenham.png data/horse_race.png