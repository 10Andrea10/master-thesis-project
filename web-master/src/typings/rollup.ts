import {edpkToIntArray, edsigToInt64Array} from '../utils/binaryConverter';
import {
  convertPublicKeys,
  numberArrayToStringArray,
  numberToHex,
} from '../utils/stringConverter';
import {Transaction} from './transaction';

export class Rollup {
  constructor(
    readonly addressesTreeRoot: number[],
    readonly balanceNonceTreeRoot: number[],
    readonly transactions: Transaction[],
    readonly publicKeys: string[],
    readonly balances: number[],
    readonly nonces: number[]
  ) {}

  public toZokratesInput() {
    const publicKeys = convertPublicKeys(this.publicKeys);
    const {transactions, transactionHelpers} = this.convertTransactions();
    const hexBalances = this.balances.map(element => numberToHex(element));
    const hexNonces = this.nonces.map(element => numberToHex(element));
    return [
      numberArrayToStringArray(this.addressesTreeRoot),
      publicKeys.map(numberArrayToStringArray),
      numberArrayToStringArray(this.balanceNonceTreeRoot),
      hexBalances,
      hexNonces,
      transactions,
      transactionHelpers,
    ];
  }

  private convertTransactions() {
    const transactions = [];
    const transactionHelpers = [];
    for (const transaction of this.transactions) {
      // const signature = edsigToInt64Array(transaction.signature).map(element =>
      //   element.toString()
      // );
      transactions.push({
        sourceIndex: '0x' + transaction.sourceIndex.toString(16),
        targetIndex: '0x' + transaction.targetIndex.toString(16),
        amount: '0x' + transaction.amount.toString(16),
        nonce: '0x' + transaction.nonce.toString(16),
      });
      transactionHelpers.push({
        sourceAddress: numberArrayToStringArray(
          edpkToIntArray(transaction.source)
        ),
        targetAddress: numberArrayToStringArray(
          edpkToIntArray(transaction.target)
        ),
        signature : transaction.signatureZokrates,
      });
    }
    return {transactions, transactionHelpers};
  }
}
