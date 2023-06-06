import {b58cdecode, prefix} from '@taquito/utils';

export function edpkToIntArray(publicKey: String): number[] {
  const pubk = Buffer.from(publicKey, 'utf-8').toString();
  const pubkDecoded = b58cdecode(pubk, prefix.edpk);
  // adds zeroes to the left of the buffer pubkDecoded
  const zeroesBuffer = Buffer.alloc(32 - pubkDecoded.length, 0);
  const pubkDecodedPadded = Buffer.concat([zeroesBuffer, pubkDecoded]);
  // Build the final array of integers
  const finalArray = [];
  // Splits the pubkDecodedPadded buffer in slices of 4 bytes and puts the result in finalArray
  for (let i = 0; i < pubkDecodedPadded.length; i += 4) {
    finalArray.push(pubkDecodedPadded.readUInt32BE(i));
  }
  return finalArray;
}
