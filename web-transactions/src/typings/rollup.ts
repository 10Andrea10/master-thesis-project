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
    return [
      this.addressesTreeRoot,
      this.publicKeys,
      this.balanceNonceTreeRoot,
      this.balances,
      this.nonces,
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
      transactions.push({
        signature: edsigToInt64Array(transaction.signature),
        operation: this.generateOperation(), // TODO: remove when operation is removed from rollup
        amount: transaction.amount.toString(16),
      });
      transactionHelpers.push({
        sourceAddress: edpkToIntArray(transaction.source),
        targetAddress: edpkToIntArray(transaction.target),
        sourceIndex: transaction.sourceIndex.toString(16),
        targetIndex: transaction.targetIndex.toString(16),
      });
    }
    return {transactions, transactionHelpers};
  }

  private generateOperation() {
    return [
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
      '0',
    ];
  }
}
