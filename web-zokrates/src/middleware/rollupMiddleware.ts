import {Request, Response} from 'express';
import {ZokratesInteractor} from '../services/zokratesInteractor';

export class RollupMiddleware {
  private readonly workDir: string = './src/zokrates';
  constructor(private readonly zokratesInteractor: ZokratesInteractor) {
    this.executeRollup = this.executeRollup.bind(this);
  }

  async executeRollup(request: Request, response: Response): Promise<void> {
    console.log(
      '[RollupMiddleware] Executing rollup with request: ',
      request.body
    );
    const computationalResult = await this.zokratesInteractor.run(
      request.body,
      './src/zokrates/rollup'
    );
    if (computationalResult.success) {
      response.send(computationalResult.result);
    } else {
      response.status(500).send(computationalResult.error);
    }
  }
}
