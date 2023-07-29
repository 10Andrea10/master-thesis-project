#!/bin/bash

# Check if an argument is provided (true/false for debug flag)
if [ $# -ne 1 ]; then
    echo "Usage: $0 <true|false>"
    exit 1
fi

# Define the version (4-6 in this case)
version="4-50"

# Function to compile Zokrates code
compile_zokrates_code() {
    local debug_flag=""
    if [ "$1" = true ]; then
        debug_flag="--debug"
    fi

    time zokrates compile -i "zk-rollup-$version.zok" -c bls12_381 $debug_flag
}

# Generate the current datetime in a format suitable for the filename
current_datetime=$(date +"%Y-%m-%d_%H-%M-%S")

# Log file path with the current datetime and version
log_file="compile_log_${version}_$current_datetime.txt"

# Call the function to compile the Zokrates code, passing the argument provided
{
    echo "Compilation started..."
    compile_zokrates_code "$1" 2>&1
    echo "Compilation completed."
} | tee "$log_file"

{
    echo "Zokrates setup started..."
    time zokrates setup -b ark -s gm17 2>&1
    echo "Zokrates setup completed."
} | tee -a "$log_file"

{
    echo "Zokrates compute-witness started..."
    time zokrates compute-witness --abi --verbose --stdin < ./../../../tests/python/output_files/rollup-$version-inputs.json 2>&1
    echo "Zokrates compute-witness completed."
} | tee -a "$log_file"

{
    echo "Zokrates generate-proof started..."
    time zokrates generate-proof -b ark -s gm17 2>&1
    echo "Zokrates generate-proof completed."
} | tee -a "$log_file"
