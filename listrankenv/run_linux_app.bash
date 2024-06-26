#!/bin/bash

# Navigate to the virtual environment root
cd "$(dirname "$0")"

# Activate the virtual environment
source bin/activate

# Navigate to the app directory and run the application
cd app
python main.py Top_50_Songs

# Deactivate the virtual environment when done
deactivate
