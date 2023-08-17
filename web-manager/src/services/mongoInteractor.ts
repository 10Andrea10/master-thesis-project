import {Collection, Document, MongoClient} from 'mongodb';
import {Transaction} from '../typings/transaction';

export class MongoInteractor {
  private transactionCollection!: Collection<Document>;

  async init(): Promise<void> {
    const client: MongoClient = new MongoClient(
      process.env.MONGODB_CONNSTRING ?? ''
    );
    await client.connect();
    const database = client.db(process.env.MONGODB_DBNAME);
    this.transactionCollection = database.collection(
      process.env.MONGODB_COLLECTION ?? ''
    );
  }
  
  /**
   * Insert a transaction. If the transaction is already present, it is not inserted.
   * @param transaction - The transaction to insert.
   */
  async insertTransaction(transaction: Transaction): Promise<void> {
    if (!(await this.isTransactionPresent(transaction))) {
      await this.transactionCollection.insertOne(transaction);
    }
  }

  /**
   * Gets all transactions.
   * @returns The list of transactions ordered by nonce.
   */
  async getTransactions(): Promise<Transaction[]> {
    const transactions = await this.transactionCollection.find().toArray();
    const transactionsList = transactions.map(transaction => {
      return new Transaction(
        transaction.signature,
        transaction.source,
        transaction.target,
        transaction.sourceIndex,
        transaction.targetIndex,
        transaction.amount,
        transaction.nonce,
        transaction.signatureZokrates
      );
    });
    // Order the transactions by nonce
    transactionsList.sort((a, b) => a.nonce - b.nonce);
    return transactionsList;
  }

  async deleteTransactions(): Promise<void> {
    await this.transactionCollection.deleteMany({});
  }

  private async isTransactionPresent(
    transaction: Transaction
  ): Promise<boolean> {
    const result = await this.transactionCollection.findOne(transaction);
    return result !== null;
  }
}
