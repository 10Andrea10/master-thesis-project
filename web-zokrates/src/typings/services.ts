import {Router} from 'express';
import {ExecutorMiddleware} from '../middleware/executorMiddleware';

export type Services = {
  router: Router;
  executorMiddleware: ExecutorMiddleware;
};

export type ComputationResult = {
  success: boolean;
  error?: string;
  result?: string;
};
