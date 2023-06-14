import {edsigToInt64Array} from '../utils/binaryConverter';
import {
  convertPublicKeys,
  numberArrayToStringArray,
  numberToHex,
} from '../utils/stringConverter';

export class Deregistration {
  constructor(
    readonly addressesTreeRoot: number[],
    readonly balanceNonceTreeRoot: number[],
    readonly publicKeys: string[],
    readonly balances: number[],
    readonly nonces: number[],
    readonly position: number,
    readonly signature: string
  ) {}

  public toZokratesInput() {
    const publicKeys = convertPublicKeys(this.publicKeys);
    const hexBalances = this.balances.map(element => numberToHex(element));
    const hexNonces = this.nonces.map(element => numberToHex(element));
    return [
      numberArrayToStringArray(this.addressesTreeRoot),
      publicKeys.map(numberArrayToStringArray),
      numberArrayToStringArray(this.balanceNonceTreeRoot),
      hexBalances,
      hexNonces,
      numberToHex(this.position),
      edsigToInt64Array(this.signature).map(element => element.toString()),
    ];
  }
}
