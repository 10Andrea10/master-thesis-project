#!/bin/bash

# Parse the arguments
version=""
debug_flag=""
initialised=""
steps=()

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -d)
            debug_flag="--debug"
            shift
            ;;
        -i)
            initialised="-initialised"
            shift
            ;;
        *)
            if [ -z "$version" ]; then
                version="$key"
            else
                steps+=("$key")
            fi
            shift
            ;;
    esac
done

# Check if the version and steps are provided
if [ -z "$version" ] || [ ${#steps[@]} -eq 0 ]; then
    echo "Usage: $0 [-d] [-i] <version> <step1> [<step2> <step3> ...]"
    exit 1
fi

# Define the function to compile Zokrates code
compile_zokrates_code() {
    local debug_flag="$1"
    local version="$2"
    cd "$version"  # Change the working directory
    time zokrates compile -i "zk-rollup-$version.zok" -c bls12_381 $debug_flag
    cd ..  # Change back to the original directory
}

compute_witness() {
    time zokrates compute-witness --abi --verbose --stdin < "./../../../tests/python/output_files/rollup$initialised-$version-inputs.json"
}

zokrates_setup() {
    time zokrates setup -b ark -s gm17
}

zokrates_generate_proof() {
    time zokrates generate-proof -b ark -s gm17
}

# Generate the current datetime in a format suitable for the filename
current_datetime=$(date +"%Y-%m-%d_%H-%M-%S")

# Log file path with the current datetime and version
log_file="./logs/zokrates_log_${version}_$current_datetime.txt"

# Function to start the mem_use script in the background and get its PID
start_mem_use_script() {
    local version="$1"
    local phase="$2"
    ./mem_use.sh "$version" "$phase" &
    mem_use_pid=$!
    echo "mem_use script started for version '$version' and phase '$phase' (PID: $mem_use_pid)."
}

# Function to stop the mem_use script gracefully using SIGTERM
stop_mem_use_script() {
    if [ -n "$mem_use_pid" ]; then
        echo "Stopping mem_use script (PID: $mem_use_pid)..."
        kill -SIGKILL "$mem_use_pid"
        wait "$mem_use_pid"  # Wait for the mem_use script to finish
        mem_use_pid=""
    fi
}

# Function to handle the SIGINT signal (Ctrl+C)
handle_ctrl_c() {
    stop_mem_use_script
    echo "Ctrl+C detected. Exiting..."
    exit 1
}

# Register the SIGINT signal handler
trap handle_ctrl_c SIGINT

# Call the respective function based on the step arguments provided
for step in "${steps[@]}"; do
    case $step in
        compile)
            {
                echo "Compilation started..."
                start_mem_use_script "$version" "compile"
                compile_zokrates_code "$debug_flag" "$version" 2>&1
                stop_mem_use_script
                echo "Compilation completed."
            } | tee -a "$log_file"
            ;;
        setup)
            {
                echo "Zokrates setup started..."
                start_mem_use_script "$version" "setup"
                cd "$version"  # Change the working directory
                zokrates_setup 2>&1
                cd ..  # Change back to the original directory
                stop_mem_use_script
                echo "Zokrates setup completed."
            } | tee -a "$log_file"
            ;;
        compute-witness)
            {
                echo "Zokrates compute-witness started..."
                start_mem_use_script "$version" "compute-witness"
                cd "$version"  # Change the working directory
                compute_witness 2>&1
                cd ..  # Change back to the original directory
                stop_mem_use_script
                echo "Zokrates compute-witness completed."
            } | tee -a "$log_file"
            ;;
        generate-proof)
            {
                echo "Zokrates generate-proof started..."
                start_mem_use_script "$version" "generate-proof"
                cd "$version"  # Change the working directory
                zokrates_generate_proof 2>&1
                cd ..  # Change back to the original directory
                stop_mem_use_script
                echo "Zokrates generate-proof completed."
            } | tee -a "$log_file"
            ;;
        *)
            echo "Invalid step '$step'. Supported steps: compile, setup, compute-witness, generate-proof"
            exit 1
            ;;
    esac
done
