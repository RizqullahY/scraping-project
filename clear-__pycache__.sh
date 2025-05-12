#!/bin/bash

find . -type d -name "__pycache__" -exec rm -rf {} +
exit 0
