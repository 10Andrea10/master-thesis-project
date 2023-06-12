import {Request, Response} from 'express';
import {MongoInteractor} from '../services/mongoInteractor';

import got from 'got';
import { TezosInteractor } from '../services/tezosInteractor';
import { Rollup } from '../typings/rollup';

export class RollupMiddleware {
  constructor(private readonly mongoInteractor: MongoInteractor,
    private readonly tezosInteractor: TezosInteractor) {
    this.executeRollup = this.executeRollup.bind(this);
  }

  async executeRollup(request: Request, response: Response): Promise<void> {
    const transactions = await this.mongoInteractor.getTransactions();
    // TODO: test
    const {publicKeys, balances, nonces} = await this.tezosInteractor.getBigMapValues();
    const addressesTreeRoot = await this.tezosInteractor.getMKRoot('mr_pub_key');
    const balanceNonceTreeRoot = await this.tezosInteractor.getMKRoot('mr_balance_nonce');
    const rollup = new Rollup(addressesTreeRoot, balanceNonceTreeRoot, transactions, publicKeys, balances, nonces);
    const zokratesInputs = rollup.toZokratesInput();
    const proof = await got.post(process.env.WEB_ROLLUP_SERVER_URL + '/execute',{
      body: JSON.stringify(zokratesInputs),
    });
    response.send(proof.body);
  }
}
