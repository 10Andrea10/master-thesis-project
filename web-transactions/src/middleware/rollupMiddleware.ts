import {Request, Response} from 'express';
import {MongoInteractor} from '../services/mongoInteractor';

import got from 'got';
import { TezosInteractor } from '../services/tezosInteractor';

export class RollupMiddleware {
  constructor(private readonly mongoInteractor: MongoInteractor,
    private readonly tezosInteractor: TezosInteractor) {
    this.executeRollup = this.executeRollup.bind(this);
  }

  async executeRollup(request: Request, response: Response): Promise<void> {
    const transactions = await this.mongoInteractor.getTransactions();
    // TODO: implement
    const {publicKeys, balances, nonces} = await this.tezosInteractor.getBigMapValues();
    const addressesTreeRoot = await this.tezosInteractor.getMKRoot('mr_pub_key');
    const balanceNonceTreeRoot = await this.tezosInteractor.getMKRoot('mr_balance_nonce');



    
    const zokratesInputs = '';
    // const proof = await got.post(process.env.WEB_ROLLUP_SERVER_URL + '/execute',{
    //   body: zokratesInputs,
    // });
    response.send('Hello world!');
  }
}
