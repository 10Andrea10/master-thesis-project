import {Router} from 'express';
import {ExecutorMiddleware} from '../middleware/executorMiddleware';
import { UserMiddleware } from '../middleware/userMiddleware';

export type Services = {
  router: Router;
  executorMiddleware: ExecutorMiddleware;
  userMiddleware: UserMiddleware;
};

export type ComputationResult = {
  success: boolean;
  error?: string;
  result?: string;
};
