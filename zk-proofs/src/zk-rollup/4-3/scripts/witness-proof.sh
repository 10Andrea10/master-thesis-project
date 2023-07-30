#!/bin/bash
zokrates compute-witness --abi --verbose --stdin < ./../../../tests/python/output_files/rollup-4-3-inputs.json
zokrates generate-proof -s gm17