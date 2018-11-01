#!/bin/bash

SCRIPT=$(readlink -f "$0")
python3 $(dirname "$SCRIPT")/app.py

