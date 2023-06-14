import {Request, Response} from 'express';
import {MongoInteractor} from '../services/mongoInteractor';

import got from 'got';
import {TezosInteractor} from '../services/tezosInteractor';
import {Rollup} from '../typings/rollup';
import {convertProof} from '../utils/proofConverter';

export class RollupMiddleware {
  constructor(
    private readonly mongoInteractor: MongoInteractor,
    private readonly tezosInteractor: TezosInteractor
  ) {
    this.executeRollup = this.executeRollup.bind(this);
  }

  async executeRollup(request: Request, response: Response): Promise<void> {
    const privateSignerKey = request.body.privateSignerKey;
    const transactions = await this.mongoInteractor.getTransactions();
    const {publicKeys, balances, nonces} =
      await this.tezosInteractor.getBigMapValues();
    const addressesTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_pub_key'
    );
    const balanceNonceTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_balance_nonce'
    );
    const rollup = new Rollup(
      addressesTreeRoot,
      balanceNonceTreeRoot,
      transactions,
      publicKeys,
      balances,
      nonces
    );
    const zokratesInputs = rollup.toZokratesInput();
    const proof = await got.post(
      process.env.WEB_ROLLUP_SERVER_URL + '/execute',
      {
        body: JSON.stringify(zokratesInputs),
        headers: {'Content-Type': 'text/plain'},
        throwHttpErrors: false,
      }
    );
    if(proof.statusCode !== 200) {
      response.status(proof.statusCode).send(proof.body);
    }

    const proofConverted = convertProof(proof.body);

    console.log('Proof converted:\n\n');
    console.log(proofConverted);
    console.log('\n\n');

    const result = await this.tezosInteractor.callRollUpSmartContract(
      "receive_rollup_proof",
      proofConverted,
      privateSignerKey
    );
    response.status(200).send(result);
  }
}
