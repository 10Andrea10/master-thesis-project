import {Request, Response} from 'express';

import got from 'got';
import {TezosInteractor} from '../services/tezosInteractor';
import {convertProof} from '../utils/proofConverter';
import {Deregistration} from '../typings/deregistration';

export class UserMiddleware {
  constructor(private readonly tezosInteractor: TezosInteractor) {
    this.deleteUser = this.deleteUser.bind(this);
  }

  async deleteUser(request: Request, response: Response): Promise<void> {
    const privateSignerKey = request.body.privateSignerKey;
    const signature = request.body.signature;
    const position = request.body.position;
    const {publicKeys, balances, nonces} =
      await this.tezosInteractor.getBigMapValues();
    const addressesTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_pub_key'
    );
    const balanceNonceTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_balance_nonce'
    );
    // TODO: 
    const rollup = new Deregistration(
        addressesTreeRoot,
        balanceNonceTreeRoot,
        publicKeys,
        balances,
        nonces,
        signature,
        position
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
    if (proof.statusCode !== 200) {
      response.status(proof.statusCode).send(proof.body);
    }

    const proofConverted = convertProof(proof.body);

    console.log('Proof converted:\n\n');
    console.log(proofConverted);
    console.log('\n\n');

    const result = await this.tezosInteractor.callRollUpSmartContract(
      proofConverted,
      privateSignerKey
    );
    response.status(200).send(result);
  }
}
