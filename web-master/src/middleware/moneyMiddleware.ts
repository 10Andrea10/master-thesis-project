import {Request, Response} from 'express';
import {TezosInteractor} from '../services/tezosInteractor';
import {numberArrayToStringArray, numberToHex} from '../utils/stringConverter';
import {convertProof} from '../utils/proofConverter';
import got from 'got';

export class MoneyMiddleware {
  constructor(private readonly tezosInteractor: TezosInteractor) {
    this.executeDeposits = this.executeDeposits.bind(this);
  }

  async executeDeposits(req: Request, res: Response): Promise<void> {
    const {balances, nonces} = await this.tezosInteractor.getBigMapValues();
    const balancesHex = balances.map(element => numberToHex(element));
    const noncesHex = nonces.map(element => numberToHex(element));
    const addressesTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_pub_key'
    );
    const balanceNonceTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_balance_nonce'
    );
    const depositQueue = await this.tezosInteractor.getDepositQueue();
    const depositQueueKeys = Array.from(depositQueue.keys());
    const depositQueueValues = Array.from(depositQueue.values());
    const depositQueueKeysHex = depositQueueKeys.map(element =>
      numberToHex(element)
    );
    const depositQueueValuesHex = depositQueueValues.map(element =>
      numberToHex(element)
    );
    const zokratesInputs = [
      numberArrayToStringArray(addressesTreeRoot),
      numberArrayToStringArray(balanceNonceTreeRoot),
      balancesHex,
      noncesHex,
      depositQueueKeysHex,
      depositQueueValuesHex,
    ];
    // const proof = await got.post(
    //   process.env.WEB_ROLLUP_SERVER_URL + '/deposit',
    //   {
    //     body: JSON.stringify(zokratesInputs),
    //     headers: {'Content-Type': 'text/plain'},
    //     throwHttpErrors: false,
    //   }
    // );
    // if (proof.statusCode !== 200) {
    //   res.status(proof.statusCode).send(proof.body);
    //   return;
    // }
    // const proofConverted = convertProof(proof.body);

    const proofConverted =
      '{"scheme":"gm17","curve":"bls12_381","proof":{"a":"0x1877749ec9c170a36d21a787d8a6a3670ba2b53931a6ab57d87ce405840e749183c69b71d6c93755debddf7be893303c00f4e8464f5b7e403f44f413ab6f4ad876cf693a973201e51ba3e4e0c7f609a5b3bf10053d1f89d5cfd8f5387d0a0569","b":"0x0019038c1d43abb1c99256bb3ac6868fec589fca4c121e5755386b524663928dbfd0231e9e9d65ff95e29647552f2909122b00dede1c0407c52776782a02ac23e1274e5fef755cbe4bdfbef85a2686936998559c86eee6d1ce64472ae1618ec501802b69bf73b94…000000000000000000000000000000000","3dd1d85b00000000000000000000000000000000000000000000000000000000","801c104700000000000000000000000000000000000000000000000000000000","0b03e68700000000000000000000000000000000000000000000000000000000","d3467e4500000000000000000000000000000000000000000000000000000000","1d72a55000000000000000000000000000000000000000000000000000000000","02124c9900000000000000000000000000000000000000000000000000000000"]}';

    throw new Error('Not implemented the call rollup contract function');
  }
}
