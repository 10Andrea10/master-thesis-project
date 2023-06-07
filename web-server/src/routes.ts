import express from 'express';
import {TransactionMiddleware} from './middleware/transactionMiddleware';
import {RollupMiddleware} from './middleware/rollupMiddleware';
import {MongoInteractor} from './services/mongoInteractor';

export const itemsRouter = express.Router();

const mongoInteractor = new MongoInteractor();
const transactionMiddleware = new TransactionMiddleware(mongoInteractor);

const rollupMiddleware = new RollupMiddleware();

/// Gets all transactions stored in the queue
itemsRouter.get('/transactions', transactionMiddleware.getAllTransactions);

// Puts a transaction in the queue
itemsRouter.put('/transactions', transactionMiddleware.addTransaction);

// Execute the rollup
itemsRouter.post('/rollup', rollupMiddleware.executeRollup);

// Execute a signature
itemsRouter.get('/sign', transactionMiddleware.signData);
