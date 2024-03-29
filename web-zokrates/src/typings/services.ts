import {Router} from 'express';
import {RollupMiddleware} from '../middleware/rollupMiddleware';
import {UserMiddleware} from '../middleware/userMiddleware';
import {MoneyMiddleware} from '../middleware/moneyMiddleware';
import {AccountsMiddleware} from '../middleware/accountsMiddleware';

export type Services = {
  router: Router;
  rollupMiddleware: RollupMiddleware;
  userMiddleware: UserMiddleware;
  moneyMiddleware: MoneyMiddleware;
  accountsMiddleware: AccountsMiddleware;
};

export type ComputationResult = {
  success: boolean;
  error?: string;
  result?: string;
};
