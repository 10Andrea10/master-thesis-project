import {Request, Response} from 'express';
import {MongoInteractor} from '../services/mongoInteractor';

export class RollupMiddleware {
  constructor(private readonly mongoInteractor: MongoInteractor) {
    this.executeRollup = this.executeRollup.bind(this);
  }

  async executeRollup(request: Request, response: Response): Promise<void> {
    const transactions = await this.mongoInteractor.getTransactions();
    response.send('Hello world!');
  }
}
