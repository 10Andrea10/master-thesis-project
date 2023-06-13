import {Request, Response} from 'express';
import {ZokratesInteractor} from '../services/zokratesInteractor';

export class ExecutorMiddleware {
  private readonly workDir: string = './src/zokrates';
  constructor(private readonly zokratesInteractor: ZokratesInteractor) {
    this.executeRollup = this.executeRollup.bind(this);
  }

  async executeRollup(request: Request, response: Response): Promise<void> {
    const computationalResult = await this.zokratesInteractor.execute(
      request.body,
      './src/zokratesRollup'
    );
    if (computationalResult.success) {
      response.send(computationalResult.result);
    } else {
      response.status(500).send(computationalResult.error);
    }
  }
}
