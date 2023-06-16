import {Request, Response} from 'express';
import {ZokratesInteractor} from '../services/zokratesInteractor';

export class MoneyMiddleware {
  constructor(private readonly zokratesInteractor: ZokratesInteractor) {
    this.executeDeposit = this.executeDeposit.bind(this);
  }

  async executeDeposit(request: Request, response: Response): Promise<void> {
    console.log(
      '[MoneyMiddleware] Executing deposit with request: ',
      request.body
    );
    const computationalResult = await this.zokratesInteractor.run(
      request.body,
      './src/zokrates/deposit'
    );

    if (computationalResult.success) {
      response.send(computationalResult.result);
    } else {
        response.status(500).send(computationalResult.error);
    }
  }
}
