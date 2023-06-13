export class Deregistration {
  constructor(
    readonly addressesTreeRoot: number[],
    readonly balanceNonceTreeRoot: number[],
    readonly publicKeys: string[],
    readonly balances: number[],
    readonly nonces: number[],
    readonly signature: string,
    readonly position: number
  ) {}

  public toZokratesInput() {
    // const publicKeys = convertPublicKeys(this.publicKeys);
    // const hexBalances: string[] = [];
    // for
  }
}
