import {Request, Response} from 'express';
import {FullTransaction} from '../typings/fullTransaction';

export async function getAllTransactions(request: Request, response: Response) {
  const transaction: FullTransaction = new FullTransaction(
    request.body.signature,
    request.body.source,
    request.body.target,
    request.body.amount,
    request.body.nonce
  );
}
export function addTransaction() {}
