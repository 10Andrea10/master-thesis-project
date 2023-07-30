import { Signature } from "./signature";

export class Transaction {
  constructor(
    readonly signature: string, // Checked only when the transaction is received. Zokrates uses signatureZokrates
    readonly source: string,
    readonly target: string,
    readonly sourceIndex: number,
    readonly targetIndex: number,
    readonly amount: number,
    readonly nonce: number,
    readonly signatureZokrates: Signature
  ) {}
}
