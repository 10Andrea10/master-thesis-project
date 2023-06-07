export class FullTransaction {
  constructor(
    readonly signature: string,
    readonly source: string,
    readonly target: string,
    readonly amount: number,
    readonly nonce: number
  ) {}
}
