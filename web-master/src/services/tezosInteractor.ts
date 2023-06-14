import {MichelsonMap, TezosToolkit} from '@taquito/taquito';
import {hexStringLittleToBigEndian} from '../utils/endianConverter';
import {Account, AccountsMapValue} from '../typings/smartContract';
import got from 'got';
import {InMemorySigner} from '@taquito/signer';

export class TezosInteractor {
  private zkRollupContract: string;
  private tezos: TezosToolkit;

  constructor() {
    if (!process.env.TEZOS_RPC_NODE_URL)
      throw new Error('Missing environment variable: TEZOS_RPC_NODE_URL');
    this.tezos = new TezosToolkit(process.env.TEZOS_RPC_NODE_URL);
    if (!process.env.ZK_ROLLUP_ADDRESS)
      throw new Error('Missing environment variable: ZK_ROLLUP_ADDRESS');
    this.zkRollupContract = process.env.ZK_ROLLUP_ADDRESS;
  }

  /**
   * Reads the storage of the zkRollup contract.
   * @param fieldName The name of the field to get the Merkle root of.
   */
  async getMKRoot(fieldName: string): Promise<number[]> {
    const contract = await this.tezos.contract.at(this.zkRollupContract);
    const root = (await contract.storage()) as any;
    const mkRootAddressesMap = root[fieldName].valueMap as Map<number, string>;

    var finalArray = [];
    for (const [, value] of mkRootAddressesMap) {
      var converted = hexStringLittleToBigEndian(value);
      finalArray.push(parseInt(converted, 16));
    }
    return finalArray;
  }

  /**
   * Fetch the public keys of all accounts in the zkRollup contract.
   * @returns The public keys ordered by their key idex.
   */
  async getPublicKeys(): Promise<string[]> {
    const storage = (await (
      await this.tezos.contract.at(this.zkRollupContract)
    ).storage()) as any;
    const bigMapId = storage['accounts'];
    const bigMap = JSON.parse(
      (
        await got.get(
          process.env.TEZOS_API_TZSTATS +
            '/explorer/bigmap/' +
            bigMapId +
            '/values'
        )
      ).body
    ) as AccountsMapValue[];
    bigMap.sort((a, b) => a.key - b.key);
    return bigMap.map(account => account.value.pub_key);
  }

  /**
   * Fetch the big map values of the zkRollup contract.
   * @returns The values, ordered by the key index.
   */
  async getBigMapValues(): Promise<{
    publicKeys: string[];
    balances: number[];
    nonces: number[];
  }> {
    const storage = (await (
      await this.tezos.contract.at(this.zkRollupContract)
    ).storage()) as any;
    const bigMapId = storage['accounts'];
    const bigMap = JSON.parse(
      (
        await got.get(
          process.env.TEZOS_API_TZSTATS +
            '/explorer/bigmap/' +
            bigMapId +
            '/values'
        )
      ).body
    ) as AccountsMapValue[];
    bigMap.sort((a, b) => a.key - b.key);
    return {
      publicKeys: bigMap.map(account => account.value.pub_key),
      balances: bigMap.map(account => account.value.mutez_balance),
      nonces: bigMap.map(account => account.value.nonce),
    };
  }

  async callRollUpSmartContract(
    entrypoint: string,
    proofConverted: any,
    privateKey: string
  ): Promise<string> {
    // Convert the proofConverted to a JSON object
    var proofConvertedJSON = JSON.parse(proofConverted);

    const inputsConverted = proofConvertedJSON.inputs;
    const inputsMichelsonMap = new MichelsonMap();
    // Add the inputs to the map
    for (let i = 0; i < inputsConverted.length; i++) {
      inputsMichelsonMap.set(i, inputsConverted[i]);
    }
    // Remove prefix 0x from the proof.a, proof.b and proof.c
    proofConvertedJSON.proof.a = proofConvertedJSON.proof.a.replace('0x', '');
    proofConvertedJSON.proof.b = proofConvertedJSON.proof.b.replace('0x', '');
    proofConvertedJSON.proof.c = proofConvertedJSON.proof.c.replace('0x', '');

    let result = '';

    try {
      this.tezos.setSignerProvider(
        await InMemorySigner.fromSecretKey(privateKey)
      );
      const contract = await this.tezos.contract.at(this.zkRollupContract);
      console.log(`Calling contract: ${this.zkRollupContract}...`);
      const operation = await contract.methods[entrypoint](
          proofConvertedJSON.proof.a,
          proofConvertedJSON.proof.b,
          proofConvertedJSON.proof.c,
          inputsMichelsonMap
        )
        .send();
      console.log(`Waiting for ${operation.hash} to be confirmed...`);
      await operation.confirmation(1);
      console.log(
        `Operation injected: https://ghostnet.tzkt.io/${operation.hash}`
      );
      result = operation.hash;
    } catch (e) {
      console.log(e);
      if (e instanceof Error) {
        result = e.message;
      }
    } finally {
      this.tezos.setSignerProvider(undefined);
    }
    return result;
  }
}
