import {Request, Response} from 'express';
import {TezosInteractor} from '../services/tezosInteractor';
import {numberArrayToStringArray, numberToHex} from '../utils/stringConverter';
import {convertProof} from '../utils/proofConverter';
import got from 'got';

export class MoneyMiddleware {
  constructor(private readonly tezosInteractor: TezosInteractor) {
    this.executeDeposits = this.executeDeposits.bind(this);
  }

  async executeDeposits(request: Request, response: Response): Promise<void> {
    const privateSignerKey = request.body.privateSignerKey;
    const {balances, nonces} = await this.tezosInteractor.getBigMapValues();
    const balancesHex = balances.map(element => numberToHex(element));
    const noncesHex = nonces.map(element => numberToHex(element));
    const addressesTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_pub_key'
    );
    const balanceNonceTreeRoot = await this.tezosInteractor.getMKRoot(
      'mr_balance_nonce'
    );
    const depositQueue = await this.tezosInteractor.getDepositQueue();
    const depositQueueKeys = Array.from(depositQueue.keys());
    const depositQueueValues = Array.from(depositQueue.values());
    const depositQueueKeysHex = depositQueueKeys.map(element =>
      numberToHex(element)
    );
    const depositQueueValuesHex = depositQueueValues.map(element =>
      numberToHex(element)
    );
    const zokratesInputs = [
      numberArrayToStringArray(addressesTreeRoot),
      numberArrayToStringArray(balanceNonceTreeRoot),
      balancesHex,
      noncesHex,
      depositQueueKeysHex,
      depositQueueValuesHex,
    ];
    // const proof = await got.post(
    //   process.env.WEB_ROLLUP_SERVER_URL + '/deposit',
    //   {
    //     body: JSON.stringify(zokratesInputs),
    //     headers: {'Content-Type': 'text/plain'},
    //     throwHttpErrors: false,
    //   }
    // );
    // if (proof.statusCode !== 200) {
    //   response.status(proof.statusCode).send(proof.body);
    //   return;
    // }
    // const proofConverted = convertProof(proof.body);

    const proofConverted =
      '{"scheme":"gm17","curve":"bls12_381","proof":{"a":"0x186dc034e40bb9ceda3573790a136d1199a615bec20450b40cba0c055c61758c210864e10852e269299ee22945ad74fd0a767f4d93bed6fe224c524286861a14c5c6d28085046fb5472eb091670e3ad0b5167a49f31c1d9d13ace675518618a5","b":"0x07c14eae6f28c0f5eade309abcd7f5f6867ec4599a541f466f1499bc36388a1193d8b848df8987de839d7fb42e38d0b510c5c56eea3b20bee6fffb32c4750528a2b645cb0bbe27699a02ecc8890736207753765025d04a770cd9a8fdda9be09e05afaf97acd8edbbcf2b96844d2be910fa6e9bea4e9e9bb9d92ee9f1634245ad87250cb0e1341fde2b9598702842877602e4d1b9a560cd8847f94896678ae74ff5a220b05bf313321b04c554d7d1dd2838f6e8e10a1bbe4ac5acd16db3517aa3","c":"0x0b53b2d87c0d1b12dbb8246661c82715a927df0d71f445c72c6ec707275ae5f07233dad89fbe3068f04d9023fd00c83b08262c0c99cac787d37cd17a5630e712619730453980a0367bf6d35a50cc0d22c4ac00985d3cab04b8366410e380106e"},"inputs":["c145ef0800000000000000000000000000000000000000000000000000000000","2acc5ff700000000000000000000000000000000000000000000000000000000","1278102d00000000000000000000000000000000000000000000000000000000","7a0239bb00000000000000000000000000000000000000000000000000000000","004a2d3f00000000000000000000000000000000000000000000000000000000","050d53ff00000000000000000000000000000000000000000000000000000000","0473569500000000000000000000000000000000000000000000000000000000","4d05a21800000000000000000000000000000000000000000000000000000000","0dabdf9300000000000000000000000000000000000000000000000000000000","cd52d5bf00000000000000000000000000000000000000000000000000000000","c23fd67e00000000000000000000000000000000000000000000000000000000","9e0a6fb600000000000000000000000000000000000000000000000000000000","cad935a500000000000000000000000000000000000000000000000000000000","5e3adadd00000000000000000000000000000000000000000000000000000000","c7f3a80f00000000000000000000000000000000000000000000000000000000","5b9ae47900000000000000000000000000000000000000000000000000000000","4d2c7d7900000000000000000000000000000000000000000000000000000000","017aac3600000000000000000000000000000000000000000000000000000000","3dd1d85b00000000000000000000000000000000000000000000000000000000","801c104700000000000000000000000000000000000000000000000000000000","0b03e68700000000000000000000000000000000000000000000000000000000","d3467e4500000000000000000000000000000000000000000000000000000000","1d72a55000000000000000000000000000000000000000000000000000000000","02124c9900000000000000000000000000000000000000000000000000000000"]}';

    console.log('Proof converted:\n\n');
    console.log(proofConverted);
    console.log('\n\n');

    const result = await this.tezosInteractor.callRollUpSmartContract(
      'receive_deposit_proof',
      proofConverted,
      privateSignerKey
    );
    response.status(200).send(result);
  }
}
