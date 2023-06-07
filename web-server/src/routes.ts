import {Services} from './typings/services';

export async function initRoutes(services: Services) {
  const {router, transactionMiddleware, rollupMiddleware} = services;

  /// Gets all transactions stored in the queue
  router.get('/transactions', transactionMiddleware.getAllTransactions);

  // Puts a transaction in the queue
  router.put('/transactions', transactionMiddleware.addTransaction);

  // Execute the rollup
  router.post('/rollup', rollupMiddleware.executeRollup);

  // Execute a signature
  router.get('/sign', transactionMiddleware.signData);
}
