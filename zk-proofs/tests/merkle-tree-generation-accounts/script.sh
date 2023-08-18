zokrates compile -c bls12_381 -i merkle-tree-generation-accounts.zok
zokrates compute-witness --abi --stdin --verbose < ./../python/output_files/user-list-256.json