import express, {Express} from 'express';

import BodyParser from 'body-parser';
import {initRoutes} from './routes';
import {MongoInteractor} from './services/mongoInteractor';
import {TransactionMiddleware} from './middleware/transactionMiddleware';
import {RollupMiddleware} from './middleware/rollupMiddleware';
import {Services} from './typings/services';

export async function init() {
  const app: Express = express();
  const port = 3000;

  app.use(BodyParser.json());

  const mongoInteractor = new MongoInteractor();
  await mongoInteractor.init();
  const transactionMiddleware = new TransactionMiddleware(mongoInteractor);
  const rollupMiddleware = new RollupMiddleware();
  const router = express.Router();

  const services: Services = {
    router,
    mongoInteractor,
    transactionMiddleware,
    rollupMiddleware,
  };

  await initRoutes(services);

  app.use('/', router);

  app.listen(port, () => {
    console.log(`[Server]: I am running at https://localhost:${port}`);
  });
}
