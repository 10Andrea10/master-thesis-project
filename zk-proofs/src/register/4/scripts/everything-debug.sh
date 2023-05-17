#!/bin/bash
zokrates compile -i register4.zok -c bls12_381 --debug
zokrates compute-witness --abi --verbose --stdin < ./../../../tests/generate-full-register-zokrates-inputs/sampleZokinput.json
zokrates setup -b ark -s gm17
zokrates generate-proof -s gm17