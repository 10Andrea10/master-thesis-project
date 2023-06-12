import {NextFunction, Request, Response} from 'express';
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
  router.post(
    '/execute',
    validateField('privateSignerKey'),
    rollupMiddleware.executeRollup
  );

  // Execute a signature
  router.get('/sign', transactionMiddleware.signData);
}

// Middleware to validate the presence of a field in the request body
function validateField(fieldName: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.body[fieldName]) {
      return res.status(400).json({error: `${fieldName} is required`});
    }
    next();
    return;
  };
}
