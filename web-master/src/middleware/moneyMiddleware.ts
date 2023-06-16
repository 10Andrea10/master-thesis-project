import {Request, Response} from 'express';
import {TezosInteractor} from '../services/tezosInteractor';
import {numberArrayToStringArray, numberToHex} from '../utils/stringConverter';
import {convertProof} from '../utils/proofConverter';
import got from 'got';

export class MoneyMiddleware {
  constructor(private readonly tezosInteractor: TezosInteractor) {
    this.executeDeposits = this.executeDeposits.bind(this);
  }

  async executeDeposits(request: Request, response: Response): Promise<void> {
    const privateSignerKey = request.body.privateSignerKey;
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
    const proof = await got.post(
      process.env.WEB_ROLLUP_SERVER_URL + '/deposit',
      {
        body: JSON.stringify(zokratesInputs),
        headers: {'Content-Type': 'text/plain'},
        throwHttpErrors: false,
      }
    );
    if (proof.statusCode !== 200) {
      response.status(proof.statusCode).send(proof.body);
      return;
    }
    const proofConverted = convertProof(proof.body);

    console.log('Proof converted:\n\n');
    console.log(proofConverted);
    console.log('\n\n');

    const result = await this.tezosInteractor.callRollUpSmartContract(
      'receive_deposit_proof',
      proofConverted,
      privateSignerKey
    );
    response.status(200).send(result);
  }
}
