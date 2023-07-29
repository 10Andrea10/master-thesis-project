#!/bin/bash
zokrates compute-witness --abi --stdin < ./../../tests/generate-full-rollup-zokrates-inputs/sampleZokinput.json
zokrates generate-proof -s gm17