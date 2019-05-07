# 此为非合约地址的签名

import logging
from cytoolz import dissoc
from hexbytes import HexBytes
from EthAccountLib_transaction import (
    UnsignedTransaction,
    encode_transaction,
    serializable_unsigned_transaction_from_dict
)


CHAIN_ID_OFFSET = 35
V_OFFSET = 27


def to_eth_v(v_raw, chain_id=None):
    if chain_id is None:
        v = v_raw + V_OFFSET
    else:
        v = v_raw + CHAIN_ID_OFFSET + 2 * chain_id
    return v

def sign_transaction_hash(account, transaction_hash, chain_id):
    signature = account.sign_msg_hash(transaction_hash)
    (v_raw, r, s) = signature.vrs
    v = to_eth_v(v_raw, chain_id)
    return (v, r, s)


def sign_transaction_dict(eth_key, transaction_dict):
    # generate RLP-serializable transaction, with defaults filled
    unsigned_transaction = serializable_unsigned_transaction_from_dict(transaction_dict)

    transaction_hash = unsigned_transaction.hash()

    # detect chain
    if isinstance(unsigned_transaction, UnsignedTransaction):
        chain_id = None
    else:
        chain_id = unsigned_transaction.v

    # sign with private key
    (v, r, s) = sign_transaction_hash(eth_key, transaction_hash, chain_id)

    # serialize transaction with rlp
    encoded_transaction = encode_transaction(unsigned_transaction, vrs=(v, r, s))

    return (v, r, s, encoded_transaction)



def signTransaction(transaction_dict, private_key):

    #这里的抽出来满足一下条件 transaction_dict是一个mapping
    #如果交易中有from地址 那么private_key得match from地址
    #因为发送交易只要rawTransaction 所以没有算交易hash
    #new_private_key是eth-keys中的对象方法

    from eth_keys import keys
    _keys = keys
    if isinstance(key, _keys.PrivateKey):
        new_private_key = private_key
    else:
        try:
            new_private_key = _keys.PrivateKey(HexBytes(key))
        except Exception as err:
            logging.error("convert key error. the private key must be exactly 32 bytes long, instead of {} bytes.".format(len(key)))
            raise

    sanitized_transaction = dissoc(transaction_dict, 'from')
    (
            v,
            r,
            s,
            rlp_encoded,
        ) = sign_transaction_dict(new_private_key, sanitized_transaction)

    signData = HexBytes(rlp_encoded)
    return signData
