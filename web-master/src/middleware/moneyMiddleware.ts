import {Request, Response} from 'express';
import {TezosInteractor} from '../services/tezosInteractor';
import {numberArrayToStringArray, numberToHex} from '../utils/stringConverter';
import {convertProof} from '../utils/proofConverter';
import got from 'got';
import {edsigToInt64Array} from '../utils/binaryConverter';
import { signPayload } from '../utils/taquito';

export class MoneyMiddleware {
  constructor(private readonly tezosInteractor: TezosInteractor) {
    this.executeDeposits = this.executeDeposits.bind(this);
    this.withdraw = this.withdraw.bind(this);
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

  async withdraw(request: Request, response: Response) {
    const privateSignerKey = request.body.privateSignerKey;
    const position = request.body.position;
    const amount = request.body.amount;
    const signature = request.body.signature;
    const {balances, nonces} = await this.tezosInteractor.getBigMapValues();
    const balancesHex = balances.map(element => numberToHex(element));
    const noncesHex = nonces.map(element => numberToHex(element));
    const addressesTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_pub_key'
    );
    const balanceNonceTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_balance_nonce'
    );
    const zokratesInputs = [
      numberArrayToStringArray(addressesTreeRoot),
      numberArrayToStringArray(balanceNonceTreeRoot),
      balancesHex,
      noncesHex,
      numberToHex(position),
      numberToHex(amount),
      edsigToInt64Array(signature).map(element => element.toString()),
    ];
    const proof = await got.post(
      process.env.WEB_ROLLUP_SERVER_URL + '/withdraw',
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
      'receive_withdraw_proof',
      proofConverted,
      privateSignerKey
    );
    response.status(200).send(result);
  }

  async signWithdraw(request: Request, response: Response): Promise<void> {
    const privateKeySource: string = request.body.privateSignerKey;
    const position: number = request.body.position;
    const amount: number = request.body.amount;
    // NOTE: trick to get the position in the right format, because
    // at least two digits are required
    const signature = await signPayload(
      position < 10
        ? '0' + position.toString()
        : position.toString() + amount.toString(),
      privateKeySource
    );
    response.send(signature);
  }
}
