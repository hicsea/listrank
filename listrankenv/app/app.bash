#!/bin/bash

# Path to the VcXsrv executable
vcxsrv_dir='/mnt/c/Program Files/VcXsrv/'
vcxsrv_file='vcxsrv.exe'

# Full path to VcXsrv
vcxsrv_path="${vcxsrv_dir}${vcxsrv_file}"

# Export DISPLAY variable
export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0

# Check if VcXsrv is already running
if pgrep -x "$vcxsrv_file" > /dev/null; then
    echo "VcXsrv is already running."
else
    # Start VcXsrv
    "$vcxsrv_path" -multiwindow -clipboard -wgl -ac &
    vcxsrv_pid=$!
    echo "VcXsrv started with PID $vcxsrv_pid."
fi

# Path to your Python virtual environment and script
venv_path='/mnt/c/Users/hicsea/Documents/UMich/Student/Coding Practice/Python/listrank/listrankenv'
script_path="${venv_path}/main.py"

# Activate the virtual environment
source "${venv_path}/bin/activate"

# Run your Python script
python3 "$script_path"


# Function to clean up processes on exit
cleanup() {
  echo "Cleaning up..."
  if [[ -n "$vcxsrv_pid" ]]; then
    kill -TERM "$vcxsrv_pid"
    wait "$vcxsrv_pid"  # Wait for the process to be terminated
  fi
  exit 0
}

# Trap SIGINT (Ctrl+C) and call cleanup function
trap cleanup SIGINT EXIT  # Also handle script exit

# Wait for Python script to finish
wait
