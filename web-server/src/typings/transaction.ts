import {ObjectId} from 'mongodb';

export class Transaction {
  constructor(
    readonly signature: string,
    readonly source: string,
    readonly target: string,
    readonly amount: number,
    readonly nonce: number,
    id?: ObjectId
  ) {}
}
