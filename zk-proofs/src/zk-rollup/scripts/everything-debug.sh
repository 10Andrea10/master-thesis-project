#!/bin/bash
zokrates compile -i zk-rollup.zok -c bls12_381 --debug
zokrates setup -b ark -s gm17
zokrates compute-witness --abi --verbose --stdin < ./../../tests/generate-full-zokrates-inputs/sampleZokinput.json
zokrates generate-proof -s gm17