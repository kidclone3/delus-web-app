#!/bin/bash

# Array to store terminal process IDs
terminal_pids=()

# Function to handle cleanup on script exit
cleanup() {
    echo "Cleaning up and exiting..."

    # Terminate all terminal processes
    for pid in "${terminal_pids[@]}"; do
        echo "Terminating process $pid"
        kill -TERM "$pid" >/dev/null 2>&1
    done

    exit 0
}
spawn_terminal() {
    xterm -hold -e  "$1" &
    echo "PID: $!"
}

# Set the trap to call the cleanup function on exit
trap cleanup INT

export PYTHONPATH=$PWD:$PWD/simulation:$PWD/simulation/data:$PWD/simulation/zeromq
# Source the virtual environment's activation script
source venv/bin/activate

# List of Python commands to run

files=( "simulation/get_destination.py" "simulation/matching_pair.py" "simulation/route_planner.py" "simulation/zeromq/mdp_broker.py")

for file in "${files[@]}"; do
    spawn_terminal "python3 $file"
    terminal_pids+=("$!")
    echo "file $file"
done


while true; do
  clear
  echo "Press [CTRL+C] to stop.."
  # shellcheck disable=SC2128
  sleep 1

done