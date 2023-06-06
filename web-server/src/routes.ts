import express from 'express';
import {
  addTransaction,
  getAllTransactions,
  signData,
} from './middleware/transactionMiddleware';
import {executeRollup} from './middleware/rollupMiddleware';

export const itemsRouter = express.Router();

/// Gets all transactions stored in the queue
itemsRouter.get('/transactions', getAllTransactions);

// Puts a transaction in the queue
itemsRouter.put('/transactions', addTransaction);

// Execute the rollup
itemsRouter.post('/rollup', executeRollup);

// Execute a signature
itemsRouter.get('/sign', signData);
