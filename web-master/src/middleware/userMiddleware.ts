import {Request, Response} from 'express';

import got from 'got';
import {TezosInteractor} from '../services/tezosInteractor';
import {convertProof} from '../utils/proofConverter';
import {Deregistration} from '../typings/deregistration';
import {
  signPayload,
  verifyDeleteUserSignature,
  verifyRegisterUserSignature,
} from '../utils/taquito';
import {Registration} from '../typings/registration';

export class UserMiddleware {
  constructor(private readonly tezosInteractor: TezosInteractor) {
    this.deleteUser = this.deleteUser.bind(this);
    this.addUser = this.addUser.bind(this);
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
    const deregistration = new Deregistration(
      addressesTreeRoot,
      balanceNonceTreeRoot,
      publicKeys,
      balances,
      nonces,
      position,
      signature
    );

    const signatureVerified = verifyDeleteUserSignature(deregistration);
    if (!signatureVerified) {
      response.status(400).send('Signature is not valid');
    }
    const zokratesInputs = deregistration.toZokratesInput();
    const proof = await got.post(
      process.env.WEB_ROLLUP_SERVER_URL + '/deregister',
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
      'receive_deregister_proof',
      proofConverted,
      privateSignerKey
    );
    response.status(200).send(result);
  }

  async addUser(request: Request, response: Response): Promise<void> {
    const privateSignerKey = request.body.privateSignerKey;
    const signature = request.body.signature;
    const position = request.body.position;
    const userPublicKey = request.body.userPublicKey;

    const {publicKeys, balances, nonces} =
      await this.tezosInteractor.getBigMapValues();
    const addressesTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_pub_key'
    );
    const balanceNonceTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_balance_nonce'
    );

    const registration = new Registration(
      addressesTreeRoot,
      balanceNonceTreeRoot,
      publicKeys,
      balances,
      nonces,
      position,
      userPublicKey,
      signature
    );

    const signatureVerified = verifyRegisterUserSignature(registration);
    if (!signatureVerified) {
      response.status(400).send('Signature is not valid');
    }

    const zokratesInputs = registration.toZokratesInput();
    const proof = await got.post(
      process.env.WEB_ROLLUP_SERVER_URL + '/register',
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
      'receive_register_proof',
      proofConverted,
      privateSignerKey,
      userPublicKey
    );
    response.send(result);
  }

  async signDeregister(request: Request, response: Response): Promise<void> {
    const privateKeySource: string = request.body.privateSignerKey;
    const position: number = request.body.position;
    // NOTE: trick to get the position in the right format, because
    // at least two digits are required
    const signature = await signPayload(
      position < 10 ? '0' + position.toString() : position.toString(),
      privateKeySource
    );
    response.send(signature);
  }

  async signRegister(request: Request, response: Response): Promise<void> {
    const privateKeySource: string = request.body.privateSignerKey;
    const position: number = request.body.position;
    const userPublicKey: string = request.body.userPublicKey;
    // NOTE: trick to get the position in the right format, because
    // at least two digits are required
    const signature = await signPayload(
      position < 10
        ? '0' + position.toString()
        : position.toString() + userPublicKey,
      privateKeySource
    );
    response.send(signature);
  }
}
