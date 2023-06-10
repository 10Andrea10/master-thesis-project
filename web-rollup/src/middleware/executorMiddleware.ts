import {Request, Response} from 'express';
import { ZokratesInteractor } from '../services/zokratesInteractor';

export class ExecutorMiddleware {

  private readonly workDir: string = "./src/zokrates";
  constructor(private readonly zokratesInteractor: ZokratesInteractor) {
    this.executeRollup = this.executeRollup.bind(this);
  }

  async executeRollup(request: Request, response: Response): Promise<void> {
    const result = await this.zokratesInteractor.execute(request.body);
    // TODO: send back the results.
    response.send('Hello world from the executor!');
  }
}
