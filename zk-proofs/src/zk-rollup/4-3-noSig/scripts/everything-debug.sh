#!/bin/bash
zokrates compile -i zk-rollup4-3.zok -c bls12_381 --debug
zokrates setup -b ark -s gm17
zokrates compute-witness --abi --verbose --stdin < ./../../../tests/generate-full-rollup-4-3-zokrates-inputs/sampleZokinput.json
zokrates generate-proof -b ark -s gm17