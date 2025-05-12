#!/bin/bash

find . -type d -name "dist" -exec rm -rf {} +
find . -type d -name "build" -exec rm -rf {} +
find . -type d -name "*.spec" -exec rm -rf {} +
exit 0
