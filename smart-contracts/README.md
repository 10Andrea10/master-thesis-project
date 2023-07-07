# Smart Contracts

This folder contains the source code of the smart contracts deployed to the Tezos blockchain.

## Taqueria

The project uses [Taqueria](https://taqueria.io). It allows to easily compile, deploy and interact with the smart contracts. It also provides an automation to run [Flextesa](https://taqueria.io/docs/plugins/plugin-flextesa/) with defined wallets and initial balances.

### Contract interaction

To interact with the smart contracts, you can use the [Taquito](https://taqueria.io/docs/plugins/plugin-taquito/) plugin. It allows to easily interact with the smart contracts from the command line. Here is an example:
1. create the file `zk-rollup.param.deposit.tz` with the following content:
```
(Pair 1 "edpku3EDFkXF2MHSipDKF2caz85yondEgqrohxdPdpXRpiX2tkFzuY")
```
2. run the following command:
```
taq transfer zk-rollup --env testing --mutez 129 --param zk-rollup.param.deposit.tz --sender bob --entrypoint deposit
```
