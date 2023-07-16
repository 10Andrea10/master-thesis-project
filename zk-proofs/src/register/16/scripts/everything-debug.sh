#!/bin/bash
zokrates compile -i register16.zok -c bls12_381
zokrates compute-witness --abi --verbose --stdin < ./../../../tests/generate-full-register-16-zokrates-inputs/sampleZokinput.json
zokrates setup -b ark -s gm17
zokrates generate-proof -s gm17