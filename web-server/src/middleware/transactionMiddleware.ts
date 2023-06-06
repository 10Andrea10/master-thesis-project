import {Request, Response} from 'express';
import {FullTransaction} from '../typings/fullTransaction';
import {signPayload} from '../utils/taquito';
import {b58cdecode, b58decode, prefix} from '@taquito/utils';
import {edpkToIntArray} from '../utils/binaryConverter';

export async function getAllTransactions() {}

export function addTransaction(request: Request, response: Response) {
  const transaction: FullTransaction = new FullTransaction(
    request.body.signature,
    request.body.source,
    request.body.target,
    request.body.amount,
    request.body.nonce
  );
}

export async function signData(request: Request, response: Response) {
  const source = 'edpkurPsQ8eUApnLUJ9ZPDvu98E8VNj4KtJa1aZr16Cr5ow5VHKnz4';
  const binarySource = edpkToIntArray(source);
  const target = 'edpkvGfYw3LyB1UcCahKQk4rF2tvbMUk8GFiTuMjL75uGXrpvKXhjn';
  const binaryTarget = edpkToIntArray(target);
  const amount = 54321;
  const nonce = 2;
  const bufferedInput = Buffer.from(
    `${binarySource}${binaryTarget}${amount}${nonce}`,
    'utf-8'
  );
  const signature = await signPayload(
    bufferedInput.toString(),
    'edsk3RFfvaFaxbHx8BMtEW1rKQcPtDML3LXjNqMNLCzC3wLC1bWbAt'
  );
  const convertedSignatureUint8Array = b58cdecode(signature, prefix.edsig);
  const convertedSingatureBuffer = Buffer.from(convertedSignatureUint8Array);
  const finalSignatureArray = [];
  // Convert the buffer to a readable integer string
  for (let i = 0; i < convertedSignatureUint8Array.length; i += 4) {
    finalSignatureArray.push(convertedSingatureBuffer.readUint32BE(i));
  }
  response.send(finalSignatureArray.toString());
}
