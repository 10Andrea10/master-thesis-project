import {Request, Response} from 'express';
import {Transaction} from '../typings/transaction';
import {signPayload, verifySignature} from '../utils/taquito';
import {b58cdecode, prefix} from '@taquito/utils';
import {edpkToIntArray} from '../utils/binaryConverter';
import {MongoInteractor} from '../services/mongoInteractor';

export class TransactionMiddleware {
  constructor(private readonly mongoInteractor: MongoInteractor) {
    this.addTransaction = this.addTransaction.bind(this);
    this.getAllTransactions = this.getAllTransactions.bind(this);
    this.deleteTransactions = this.deleteTransactions.bind(this);
    this.signData = this.signData.bind(this);
  }

  async addTransaction(request: Request, response: Response): Promise<void> {
    const transaction: Transaction = new Transaction(
      request.body.signature,
      request.body.source,
      request.body.target,
      request.body.amount,
      request.body.nonce
    );
    const signatureVerified = verifySignature(transaction);
    if (!signatureVerified) {
      response.status(400).send('Signature is not valid');
    }
    await this.mongoInteractor.insertTransaction(transaction);
    response.send();
  }

  async getAllTransactions(
    request: Request,
    response: Response
  ): Promise<void> {
    const transactions = await this.mongoInteractor.getTransactions();
    response.send(transactions);
  }

  async deleteTransactions(
    request: Request,
    response: Response
  ): Promise<void> {
    await this.mongoInteractor.deleteTransactions();
    response.send();
  }

  async signData(request: Request, response: Response): Promise<void> {
    const binarySource = edpkToIntArray(request.body.source);
    const binaryTarget = edpkToIntArray(request.body.target);
    const amount: string = request.body.amount;
    const nonce: string = request.body.nonce;
    const privateKeySource: string = request.body.privateKey;
    const bufferedInput = Buffer.from(
      `${binarySource}${binaryTarget}${amount}${nonce}`,
      'utf-8'
    );
    const signature = await signPayload(
      bufferedInput.toString(),
      privateKeySource //'edsk3RFfvaFaxbHx8BMtEW1rKQcPtDML3LXjNqMNLCzC3wLC1bWbAt'
    );
    response.send(signature);
  }
}
