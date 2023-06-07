import {Request, Response} from 'express';
import {FullTransaction} from '../typings/fullTransaction';
import {signPayload, verifySignature} from '../utils/taquito';
import {b58cdecode, prefix} from '@taquito/utils';
import {edpkToIntArray} from '../utils/binaryConverter';
import {MongoInteractor} from '../services/mongoInteractor';

export class TransactionMiddleware {
  constructor(private readonly mongoInteractor: MongoInteractor) {}

  addTransaction(request: Request, response: Response) {
    const transaction: FullTransaction = new FullTransaction(
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
  }

  getAllTransactions(request: Request, response: Response) {}

  async signData(request: Request, response: Response) {
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
    const convertedSignatureUint8Array = b58cdecode(signature, prefix.edsig);
    const convertedSingatureBuffer = Buffer.from(convertedSignatureUint8Array);
    const finalSignatureArray = [];
    // Convert the buffer to a readable integer string
    for (let i = 0; i < convertedSignatureUint8Array.length; i += 8) {
      finalSignatureArray.push(convertedSingatureBuffer.readBigUint64BE(i));
    }
    response.send(finalSignatureArray.toString());
  }
}
