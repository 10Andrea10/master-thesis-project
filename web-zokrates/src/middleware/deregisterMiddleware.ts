import {Request, Response} from 'express';
import {ZokratesInteractor} from '../services/zokratesInteractor';

export class DeregisterMiddleware {
  constructor(private readonly zokratesInteractor: ZokratesInteractor) {
    this.deregisterUser = this.deregisterUser.bind(this);
  }

  async deregisterUser(request: Request, response: Response): Promise<void> {
    console.log(
      '[DeregisterMiddleware] Deregistering user with request: ',
      request.body
    );
    const computationalResult = await this.zokratesInteractor.run(
      request.body,
      './src/zokratesDeregister'
    );
    if (computationalResult.success) {
      response.send(computationalResult.result);
    } else {
      response.status(500).send(computationalResult.error);
    }
  }
}
