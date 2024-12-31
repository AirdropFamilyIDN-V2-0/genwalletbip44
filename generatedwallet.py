from eth_account import Account
from web3 import Web3
from bip_utils import Bip39SeedGenerator, Bip44Coins, Bip44, base58, Bip44Changes

web3 = Web3()
web3.eth.account.enable_unaudited_hdwallet_features()

#log to txt file
def log(txt):
    f = open('generatedwallet.txt', "a")
    f.write(txt + '\n')
    f.close()

class BlockChainAccount():
    def __init__(self, mnemonic, coin_type=Bip44Coins.ETHEREUM, password='') -> None:
        self.mnemonic = mnemonic.strip()
        self.coin_type = coin_type
        self.password = password # if have password

    def get_address_pk(self):
        seed_bytes = Bip39SeedGenerator(self.mnemonic).Generate(self.password)
        if self.coin_type != Bip44Coins.SOLANA:
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, self.coin_type).DeriveDefaultPath()
            return bip44_mst_ctx.PublicKey().ToAddress(), bip44_mst_ctx.PrivateKey().Raw().ToHex()
        else:
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, self.coin_type)
           
            bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
            bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT) # if you use "Solflare", remove this line and make a simple code modify and test
            priv_key_bytes = bip44_chg_ctx.PrivateKey().Raw().ToBytes()
            public_key_bytes = bip44_chg_ctx.PublicKey().RawCompressed().ToBytes()[1:]
            key_pair = priv_key_bytes+public_key_bytes


            return bip44_chg_ctx.PublicKey().ToAddress(), base58.Base58Encoder.Encode(key_pair)

coin_types = {
    Bip44Coins.BITCOIN: "Bitcoin",
    Bip44Coins.COSMOS: "Cosmos",
    Bip44Coins.DOGECOIN: "Dogecoin",
    Bip44Coins.ETHEREUM: "Ethereum",
    Bip44Coins.KAVA: "Kava",
    Bip44Coins.LITECOIN: "Litecoin",
    Bip44Coins.NEAR_PROTOCOL: "Near Protocol",
    Bip44Coins.RIPPLE: "Ripple",
    Bip44Coins.SOLANA: "Solana",
    Bip44Coins.TRON: "Tron",
}

print(f'Generate Wallet Multiple Chain')
loop = input("How Many You Want Generate Wallet ? : ")
for i in range(0,int(loop)):
    for coin_type in coin_types.keys():
        chain_name = coin_types[coin_type]
        acct, mnemonic = Account.create_with_mnemonic()
        bca = BlockChainAccount(mnemonic=mnemonic, coin_type=coin_type)
        address, pk = bca.get_address_pk()
        log(f'{chain_name} Mainnet Address : {address}')
        log(f'Phrase/Mnemonic 12 Word : {mnemonic}')
        log(f'Privatekey : {pk}')
        log('-----------------------------------------------')
        print(f'Generate Wallet {i} Success')
        print(f'Your Address, 12 Word Phrase/Mnemonic & Privatekey Saved To File')
