import {Request, Response} from 'express';

export class ExecutorMiddleware {
  constructor() {
    this.executeRollup = this.executeRollup.bind(this);
  }

  async executeRollup(request: Request, response: Response): Promise<void> {
    response.send('Hello world from the executor!');
  }
}
