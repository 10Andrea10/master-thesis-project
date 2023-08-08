zokrates compile -c bls12_381 -i transaction-hash-generation.zok
zokrates compute-witness --verbose --abi --stdin < ./../python/output_files/transactions-plain.json > witness.txt