import {verifySignature as verifySignatureTaquito} from '@taquito/utils';
import {InMemorySigner} from '@taquito/signer';
import {Transaction} from '../typings/transaction';
import {edpkToIntArray} from './binaryConverter';
import {Deregistration} from '../typings/deregistration';
import {Registration} from '../typings/registration';

export function verifyTransactionSignature(transaction: Transaction): boolean {
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

export function verifyDeleteUserSignature(
  deregistration: Deregistration
): boolean {
  const buffer = Buffer.from(
    deregistration.position < 10
      ? `0${deregistration.position}`
      : `${deregistration.position}`,
    'utf-8'
  );
  return verifySignatureTaquito(
    buffer.toString(),
    deregistration.publicKeys[deregistration.position],
    deregistration.signature
  );
}

export function verifyRegisterUserSignature(
  registration: Registration
): boolean {
  const buffer = Buffer.from(
    registration.position < 10
      ? `0${registration.position}`
      : `${registration.position}` + registration.userPublicKey,
    'utf-8'
  );
  return verifySignatureTaquito(
    buffer.toString(),
    registration.userPublicKey,
    registration.signature
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
