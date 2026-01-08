#!/bin/bash

# Get the absolute path to the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set the PYTHONPATH to include the built modules
# We point to 'python' where we fixed the module structure
export PYTHONPATH=$PYTHONPATH:$SCRIPT_DIR/gr-rfid/build/python

# Set LD_LIBRARY_PATH for C++ shared libraries
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$SCRIPT_DIR/gr-rfid/build/lib

echo "Setting up environment..."
echo "PYTHONPATH set to include: $SCRIPT_DIR/gr-rfid/build/python"

# Run the reader script
# -E preserves the environment variables (like PYTHONPATH) when switching to sudo
# GR_SCHEDULER=STS and nice -n -20 are for real-time priority
echo "Starting Reader..."
cd $SCRIPT_DIR/gr-rfid/apps
sudo LD_LIBRARY_PATH=$LD_LIBRARY_PATH PYTHONPATH=$PYTHONPATH GR_SCHEDULER=STS nice -n -20 python3 -u reader.py
