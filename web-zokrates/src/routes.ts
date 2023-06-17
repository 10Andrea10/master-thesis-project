import {Services} from './typings/services';

export async function initRoutes(services: Services) {
  const {router, rollupMiddleware, userMiddleware, moneyMiddleware} = services;

  // Execute the rollup
  router.post('/execute', rollupMiddleware.executeRollup);

  router.post('/deregister', userMiddleware.deregisterUser);

  router.post('/register', userMiddleware.registerUser);

  router.post('/deposit', moneyMiddleware.executeDeposit);

  router.post('/withdraw', moneyMiddleware.executeWithdraw);
}
