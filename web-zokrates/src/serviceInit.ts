import express, {Express} from 'express';

import BodyParser from 'body-parser';
import {initRoutes} from './routes';
import {Services} from './typings/services';
import { RollupMiddleware } from './middleware/rollupMiddleware';
import { ZokratesInteractor } from './services/zokratesInteractor';
import { UserMiddleware } from './middleware/userMiddleware';
import { MoneyMiddleware } from './middleware/moneyMiddleware';

export async function init() {
  const app: Express = express();
  const port = 3005;

  // app.use(BodyParser.json());
  app.use(BodyParser.text());

  // Initialize the services
  const zokratesInteractor = new ZokratesInteractor();
  const rollupMiddleware = new RollupMiddleware(zokratesInteractor);
  const userMiddleware = new UserMiddleware(zokratesInteractor);
  const moneyMiddleware = new MoneyMiddleware(zokratesInteractor);

  const router = express.Router();

  const services: Services = {
    router,
    rollupMiddleware,
    userMiddleware,
    moneyMiddleware,
  };

  await initRoutes(services);

  app.use('/', router );

  app.listen(port, () => {
    console.log(`[Rollup Server]: I am running at https://localhost:${port}`);
  });
}
