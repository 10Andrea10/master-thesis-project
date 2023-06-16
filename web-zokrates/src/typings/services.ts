import {Router} from 'express';
import {RollupMiddleware} from '../middleware/rollupMiddleware';
import { UserMiddleware } from '../middleware/userMiddleware';

export type Services = {
  router: Router;
  rollupMiddleware: RollupMiddleware;
  userMiddleware: UserMiddleware;
};

export type ComputationResult = {
  success: boolean;
  error?: string;
  result?: string;
};
