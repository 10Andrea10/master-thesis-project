import {Router} from 'express';
import { ExecutorMiddleware } from '../middleware/executorMiddleware';

export type Services = {
  router: Router;
  executorMiddleware: ExecutorMiddleware;
};
