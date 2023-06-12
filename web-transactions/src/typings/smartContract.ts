export type Account = {
  mutez_balance: number;
  nonce: number;
  pub_key: string;
};

export type AccountsMapValue = {
    key: number;
    hahs: string;
    value: Account;
}