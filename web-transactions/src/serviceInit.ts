import express, {Express} from 'express';

import BodyParser from 'body-parser';
import {initRoutes} from './routes';
import {MongoInteractor} from './services/mongoInteractor';
import {TransactionMiddleware} from './middleware/transactionMiddleware';
import {RollupMiddleware} from './middleware/rollupMiddleware';
import {Services} from './typings/services';
import {TezosInteractor} from './services/tezosInteractor';

export async function init() {
  const app: Express = express();
  const port = 3000;

  app.use(BodyParser.json());

  // Initialize the services

  const mongoInteractor = new MongoInteractor();
  await mongoInteractor.init();
  const transactionMiddleware = new TransactionMiddleware(mongoInteractor);
  const tezosInteractor = new TezosInteractor();
  const rollupMiddleware = new RollupMiddleware(
    mongoInteractor,
    tezosInteractor
  );
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
    console.log(`[Web Server]: I am running at https://localhost:${port}`);
  });
}
