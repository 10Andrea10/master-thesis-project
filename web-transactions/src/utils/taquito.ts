import {verifySignature as verifySignatureTaquito} from '@taquito/utils';
import {InMemorySigner} from '@taquito/signer';
import {Transaction} from '../typings/transaction';
import {edpkToIntArray} from './binaryConverter';

export function verifySignature(transaction: Transaction): boolean {
  const binarySource = edpkToIntArray(transaction.source);
  const binaryTarget = edpkToIntArray(transaction.target);
  const amount = transaction.amount;
  const nonce = transaction.nonce;
  const bufferedInput = Buffer.from(
    `${binarySource}${binaryTarget}${amount}${nonce}`,
    'utf-8'
  );
  return verifySignatureTaquito(
    bufferedInput.toString(),
    transaction.source,
    transaction.signature
  );
}

export async function signPayload(
  payload: string,
  privateKey: string
): Promise<string> {
  const signer = new InMemorySigner(privateKey);
  const signature = await signer.sign(payload);
  return signature.prefixSig;
}
