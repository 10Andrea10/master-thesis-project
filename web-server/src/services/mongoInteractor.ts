import {Collection, Document, MongoClient} from 'mongodb';

export class MongoInteractor {
  transactionCollection?: Collection<Document>;

  async init() {
    const client: MongoClient = new MongoClient(
      process.env.DB_CONN_STRING ?? ''
    );
    await client.connect();
    const database = client.db(process.env.MONGODB_DBNAME);
    this.transactionCollection = database.collection(
      process.env.MONGODB_COLLECTION ?? ''
    );
  }
}
