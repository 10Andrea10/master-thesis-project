import {Router} from 'express';
import {MongoInteractor} from '../services/mongoInteractor';
import {TransactionMiddleware} from '../middleware/transactionMiddleware';
import {RollupMiddleware} from '../middleware/rollupMiddleware';

export type Services = {
  router: Router;
  mongoInteractor: MongoInteractor;
  transactionMiddleware: TransactionMiddleware;
  rollupMiddleware: RollupMiddleware;
};
