import {Request, Response} from 'express';
import { ZokratesInteractor } from '../services/zokratesInteractor';

export class DeregisterMiddleware {

  constructor(private readonly zokratesInteractor: ZokratesInteractor) {
    this.deregisterUser = this.deregisterUser.bind(this);
  }

  async deregisterUser(request: Request, response: Response): Promise<void> {
    const computationalResult = await this.zokratesInteractor.execute(request.body, "./src/zokratesDeregister");
    if(computationalResult.success) {
      response.send(computationalResult.result);
    } else {
      response.status(500).send(computationalResult.error);
    }
  }
}
