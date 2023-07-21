#!/bin/bash

# Check if an argument is provided (true/false for debug flag)
if [ $# -ne 1 ]; then
    echo "Usage: $0 <true|false>"
    exit 1
fi

# Function to compile Zokrates code
compile_zokrates_code() {
    local debug_flag=""
    if [ "$1" = true ]; then
        debug_flag="--debug"
    fi

    zokrates compile -i zk-rollup16-3.zok -c bls12_381 $debug_flag
}

# Call the function to compile the Zokrates code, passing the argument provided
compile_zokrates_code "$1"
zokrates setup -b ark -s gm17
zokrates compute-witness --abi --verbose --stdin < ./../../../tests/python/output_files/rollup-16-3-inputs.json
zokrates generate-proof -b ark -s gm17


