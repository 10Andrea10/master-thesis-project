import {Services} from './typings/services';

export async function initRoutes(services: Services) {
  const {router, transactionMiddleware, rollupMiddleware} = services;

  /// Gets all transactions stored in the queue
  router.get('/transactions', transactionMiddleware.getAllTransactions);

  // Puts a transaction in the queue
  router.put('/transactions', transactionMiddleware.addTransaction);

  // Deletes all transactions in the queue
  // NOTE: This is a temporary endpoint for testing purposes
  router.delete('/transactions', transactionMiddleware.deleteTransactions);

  // Execute the rollup
  router.post('/execute', rollupMiddleware.executeRollup);

  // Execute a signature
  router.get('/sign', transactionMiddleware.signData);
}
