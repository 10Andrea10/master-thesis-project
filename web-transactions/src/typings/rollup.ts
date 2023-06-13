import {edpkToIntArray, edsigToInt64Array} from '../utils/binaryConverter';
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
    const publicKeys = this.convertPublicKeys();
    const {transactions, transactionHelpers} = this.convertTransactions();
    const hexBalances: string[] = [];
    for (const balance of this.balances) {
      // NOTE: I have no idea why this is necessary, but it is.
      // If I do balance.toString(16) does not convert to hex at all.
      const tmp = balance.toString();
      const tmp2 = parseInt(tmp);
      const tmp3 = tmp2.toString(16);
      hexBalances.push("0x" + tmp3);
    }
    const hexNonces = [];
    for (const nonce of this.nonces) {
      const tmp = nonce.toString();
      const tmp2 = parseInt(tmp);
      const tmp3 = tmp2.toString(16);
      hexNonces.push("0x" + tmp3);
    }
    return [
      this.numberArrayToStringArray(this.addressesTreeRoot),
      publicKeys.map(this.numberArrayToStringArray),
      this.numberArrayToStringArray(this.balanceNonceTreeRoot),
      hexBalances,
      hexNonces,
      transactions,
      transactionHelpers,
    ];
  }

  private convertPublicKeys(): number[][] {
    const publicKeys = [];
    for (const publicKey of this.publicKeys) {
      publicKeys.push(edpkToIntArray(publicKey));
    }
    return publicKeys;
  }

  private convertTransactions() {
    const transactions = [];
    const transactionHelpers = [];
    for (const transaction of this.transactions) {
      const signature = edsigToInt64Array(transaction.signature).map(element =>
        element.toString()
      );
      transactions.push({
        sourceIndex: "0x" + transaction.sourceIndex.toString(16),
        targetIndex: "0x" + transaction.targetIndex.toString(16),
        amount: "0x" + transaction.amount.toString(16),
        nonce: "0x" + transaction.nonce.toString(16),
      });
      transactionHelpers.push({
        sourceAddress: this.numberArrayToStringArray(
          edpkToIntArray(transaction.source)
        ),
        targetAddress: this.numberArrayToStringArray(
          edpkToIntArray(transaction.target)
        ),
        signature,
      });
    }
    return {transactions, transactionHelpers};
  }

  private numberArrayToStringArray(numberArray: number[]) {
    return numberArray.map(element => element.toString());
  }
}
