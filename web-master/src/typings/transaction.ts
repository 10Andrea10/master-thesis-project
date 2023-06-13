export class Transaction {
  constructor(
    readonly signature: string,
    readonly source: string,
    readonly target: string,
    readonly sourceIndex: number,
    readonly targetIndex: number,
    readonly amount: number,
    readonly nonce: number
  ) {}
}
