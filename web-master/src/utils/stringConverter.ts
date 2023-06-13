import {edpkToIntArray} from './binaryConverter';

export function convertPublicKeys(publicKeys: string[]): number[][] {
  const publicKeysConverted = [];
  for (const publicKey of publicKeys) {
    publicKeysConverted.push(edpkToIntArray(publicKey));
  }
  return publicKeysConverted;
}

export function numberArrayToStringArray(numberArray: number[]) {
  return numberArray.map(element => element.toString());
}

export function numberToHex(number: number) {
    // NOTE: this is a hack to convert a number to hex because the built-in
    // function number.toString(16) does not work. )-;
  const tmp = number.toString();
  const tmp2 = parseInt(tmp);
  const tmp3 = tmp2.toString(16);
  return "0x" + tmp3;
}
