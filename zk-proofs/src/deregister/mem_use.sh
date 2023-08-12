#!/bin/bash

# Function to handle SIGTERM signal and terminate gracefully
handle_sigterm() {
    echo "Received SIGTERM signal. Terminating gracefully..."
    exit 0
}

# Trap the SIGTERM signal to handle termination gracefully
trap handle_sigterm SIGTERM

# Get the version and phase from the arguments passed by the second script
version="$1"
phase="$2"

# Generate the current datetime in a format suitable for the filename
current_datetime=$(date +"%Y-%m-%d_%H-%M-%S")

# Log file path with the current datetime, version, and phase
log_file="./logs/mem_log_${version}_${phase}_$current_datetime.txt"

# Infinite loop to monitor RAM and Swap usage every 60 seconds
while true; do
    # Get the current date and time
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # Get RAM usage information using the 'free' command, and extract used, and free columns
    ram_info=$(free -h | awk '/^Mem:/ {print $3, $4}')

    # Get Swap usage information using the 'free' command, and extract used, and free columns
    swap_info=$(free -h | awk '/^Swap:/ {print $3, $4}')

    # Append the timestamp, RAM usage, and Swap usage info to the log file
    echo "$timestamp RAM: $ram_info ====== SWAP: $swap_info" >> "$log_file"

    # Sleep for 60 seconds before the next measurement
    sleep 60
done
