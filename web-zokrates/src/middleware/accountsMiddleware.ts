import {Request, Response} from 'express';
import {ZokratesInteractor} from '../services/zokratesInteractor';

export class AccountsMiddleware {
  constructor(private readonly zokratesInteractor: ZokratesInteractor) {
    this.executeEnlarge = this.executeEnlarge.bind(this);
  }

  async executeEnlarge(request: Request, response: Response): Promise<void> {
    console.log(
      '[AccountsMiddleware] Executing enlarge with request:\n',
      request.body
    );
    const computationalResult = await this.zokratesInteractor.run(
      request.body,
      './src/zokrates/enlarge'
    );

    if (computationalResult.success) {
      response.send(computationalResult.result);
    } else {
      response.status(500).send(computationalResult.error);
    }
  }
}
