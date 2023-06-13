import {Router} from 'express';
import {ExecutorMiddleware} from '../middleware/executorMiddleware';
import { DeregisterMiddleware } from '../middleware/deregisterMiddleware';

export type Services = {
  router: Router;
  executorMiddleware: ExecutorMiddleware;
  deregisterMiddleware: DeregisterMiddleware;
};

export type ComputationResult = {
  success: boolean;
  error?: string;
  result?: string;
};
