import {Request, Response} from 'express';
import {ZokratesInteractor} from '../services/zokratesInteractor';

export class UserMiddleware {
  constructor(private readonly zokratesInteractor: ZokratesInteractor) {
    this.deregisterUser = this.deregisterUser.bind(this);
    this.registerUser = this.registerUser.bind(this);
  }

  async deregisterUser(request: Request, response: Response): Promise<void> {
    console.log(
      '[UserMiddleware] Deregistering user with request:\n ',
      request.body
    );
    const computationalResult = await this.zokratesInteractor.run(
      request.body,
      './src/zokrates/deregister'
    );
    if (computationalResult.success) {
      response.send(computationalResult.result);
    } else {
      response.status(500).send(computationalResult.error);
    }
  }

  async registerUser(request: Request, response: Response): Promise<void> {
    console.log(
      '[UserMiddleware] Registering user with request:\n ',
      request.body
    );
    const computationalResult = await this.zokratesInteractor.run(
      request.body,
      './src/zokrates/register'
    );
    if (computationalResult.success) {
      response.send(computationalResult.result);
    } else {
      response.status(500).send(computationalResult.error);
    }
  }
}
