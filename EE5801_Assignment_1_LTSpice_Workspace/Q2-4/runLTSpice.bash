#!/bin/bash

# Path to LTspice executable
LTSPICE_PATH="/c/Program Files/LTC/LTspiceXVII/XVIIx64.exe"

# Find all .cir files and run them with LTspice
for file in *.cir; do
  "$LTSPICE_PATH" "$file"
done