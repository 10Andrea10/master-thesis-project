#!/bin/bash
zokrates compile -i zk-rollup.zok -c bls12_381
zokrates setup -b ark -s gm17
zokrates compute-witness --abi --verbose --stdin < ./../../../tests/python/output_files/rollup-4-3-inputs.json
zokrates generate-proof -s gm17