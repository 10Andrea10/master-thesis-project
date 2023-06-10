import express, {Express} from 'express';

import BodyParser from 'body-parser';
import {initRoutes} from './routes';
import {Services} from './typings/services';
import { ExecutorMiddleware } from './middleware/executorMiddleware';

export async function init() {
  const app: Express = express();
  const port = 3005;

  app.use(BodyParser.json());

  // Initialize the services
  const executorMiddleware = new ExecutorMiddleware();

  const router = express.Router();

  const services: Services = {
    router,
    executorMiddleware
  };

  await initRoutes(services);

  app.use('/', router );

  app.listen(port, () => {
    console.log(`[Rollup Server]: I am running at https://localhost:${port}`);
  });
}