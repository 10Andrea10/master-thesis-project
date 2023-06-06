import {verifySignature as verifySignatureTaquito} from '@taquito/utils';
import {InMemorySigner} from '@taquito/signer';

export function verifySignature(
  payload: string,
  publicKey: string,
  signature: string
): boolean {
  return verifySignatureTaquito(payload, publicKey, signature);
}

export async function signPayload(
  payload: string,
  privateKey: string
): Promise<string> {
  const signer = new InMemorySigner(privateKey);
  const signature = await signer.sign(payload);
  return signature.prefixSig;
}
