import re
import sha3
import base64
from ecdsa import SigningKey, SECP256k1
from Crypto.Cipher import AES


#pysha3 ecdsa  pycryptodome

'''
Notice:
首先加密是pycryptodome因为pycryto不再维护了
关于ETH的地址公私钥对,地址校验 签名

公私钥对:
查看https://ethfans.org/posts/basic-cryptography-of-wallet获取ETH公私钥的描述
通过椭圆曲线算法生成钥匙对（公钥和私钥），以太坊采用的是secp256k1曲线。公钥采用uncompressed模式，生成的私钥为长度32的16进制字串，公钥为长度64的公钥字串。公钥04开头。
把公钥去掉04，剩下的进行keccak-256的哈希，得到长度64的16进制字串，丢掉前面24个，拿后40个，再加上"0x"，即为以太坊地址。
整个过程可以归纳为：
Get Private-key
Private-key -> Public-key
Public-key -> Address

关于地址校验 签名:
ETH有官方的web3.py库。这个库是利用本地或者远程节点。然后封装了节点的rpc方法去与节点交互
但是  查看这个库的源码可以发现
离线签名是调用了官方的eth_account库--但是这个库又调用了eth-util和eth-keys。这个库也有生成公私钥对方法
地址校验是调用了官方的eth_utils库。这个库有地址的校验方法

最后https://github.com/mathiasestolarz/eth-address-gen/有现成的python生成公私钥对和地址校验的方法
而且也调用了官方的eth_keys库(这个库可以已知私钥推导出地址)

https://github.com/rmeissner/py-eth-sig-utils这个签名工具也是调用了官方的  ethereum库

妈个比真是麻烦  eth-utils eth-keys eth-account这三个库互相之间乱调用
'''


class AESCipher(object):
    def __init__(self, key):
        self.cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)

    def encrypt(self, raw):
        encrypted = self.cipher.encrypt(raw.encode('utf-8'))
        encoded = base64.b64encode(encrypted)
        ret = str(encoded, 'utf-8')
        return ret

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        decrypted = self.cipher.decrypt(decoded)
        ret = str(decrypted, 'utf-8')
        return ret


def generate_raw_pair():
    keccak = sha3.keccak_256()
    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()
    keccak.update(pub)
    address = keccak.hexdigest()[24:]
    privkey = priv.to_string().hex()
    address = '0x' + address
    return privkey, address


def generate_wallet(mypass):  # 16 24 32位字符串
    privkey, address = generate_raw_pair()
    aes = AESCipher(mypass)
    enPrivkey = aes.encrypt(privkey)
    return address, enPrivkey


def decipher_key(mypass, enPrivkey):
    aes = AESCipher(mypass)
    privkey = aes.decrypt(enPrivkey)
    return privkey

# Takes a hex (string) address as input
# 暂时不支持二进制地址  对于用户来说没必要那么深 前端展示也不直观
# 输出大小写混编的地址
def checksum_encode(addr_str):
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out

# Takes a hex (string) address as input
def validateAddress(addr):
    pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
    return False if (not isinstance(addr,str) or not pattern.match(addr) or addr != checksum_encode(addr)) else True




# MyPASS:GongXiFaCaiGoodGoodStudyDayDayUp
# mypass = os.environ.get('MYPASS')  mypass must be 32 bytes
# address, enPrivkey = generate_wallet(mypass)
# privkey = decipher_key(mypass, enPrivkey)
