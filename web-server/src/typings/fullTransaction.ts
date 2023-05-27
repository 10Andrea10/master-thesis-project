export class FullTransaction {
  constructor(
    readonly signature: String,
    readonly sourcePublicKey: String,
    readonly targetPublicKey: String,
    readonly amount: number,
    readonly nonce: number
  ) {}
}
