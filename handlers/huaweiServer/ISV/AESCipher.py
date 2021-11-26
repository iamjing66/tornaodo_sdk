import base64
import hashlib
from Crypto.Cipher import AES


class AES_Turbe:

    def __init__(self, key: str , iv : str):
        """Init aes object used by encrypt or decrypt.
        AES/ECB/PKCS5Padding  same as aes in java default.
        """

        #self.aes = _AES.new(self.get_sha1prng_key(key), _AES.MODE_CBC,iv.encode())
        enkey = self.get_sha1prng_key(key)
        print("enkey = " , enkey)
        self.aes = AES.new(key=enkey, mode=AES.MODE_CBC, IV=iv.encode("utf-8"))

    @staticmethod
    def get_sha1prng_key(key: str) -> bytes:
        """encrypt key with SHA1PRNG.
        same as java AES crypto key generator SHA1PRNG.
        SecureRandom secureRandom = SecureRandom.getInstance("SHA1PRNG" );
        secureRandom.setSeed(decryptKey.getBytes());
        keygen.init(128, secureRandom);
        :param string key: original key.
        :return bytes: encrypt key with SHA1PRNG, 128 bits or 16 long bytes.
        """

        signature: bytes = hashlib.sha1(key.encode("utf-8")).digest()
        signature: bytes = hashlib.sha1(signature).digest()
        return signature[:16]

    @staticmethod
    def padding(s: str) -> str:
        """Padding PKCS5"""

        pad_num: int = 16 - len(s) % 16
        return s + pad_num * chr(pad_num)

    @staticmethod
    def unpadding(s):
        """Unpadding PKCS5"""

        padding_num: int = ord(s[-1])
        return s[: -padding_num]

    def encrypt_to_bytes(self, content_str):
        """From string encrypt to bytes ciphertext.
        """

        content_bytes = self.padding(content_str).encode("utf-8")
        ciphertext_bytes = self.aes.encrypt(content_bytes)
        return ciphertext_bytes

    def encrypt_to_base64(self, content_str):
        """From string encrypt to base64 ciphertext.
        """

        ciphertext_bytes = self.encrypt_to_bytes(content_str)
        ciphertext_bs64 = base64.b64encode(ciphertext_bytes).decode("utf-8")
        return ciphertext_bs64

    def decrypt_from_bytes(self, ciphertext_bytes):
        """From bytes ciphertext decrypt to string.
        """

        content_bytes = self.aes.decrypt(ciphertext_bytes)
        content_str = self.unpadding(content_bytes.decode("utf-8"))
        return content_str

    def decrypt_from_base64(self, ciphertext_bs64):
        """From base64 ciphertext decrypt to string.
        """

        ciphertext_bytes = base64.b64decode(ciphertext_bs64)
        content_str = self.decrypt_from_bytes(ciphertext_bytes)
        return content_str


def encrypt_to_bytes(content_str, encrypt_key: str):
    """From string encrypt to bytes ciphertext.
    """

    aes: AES = AES(encrypt_key)
    ciphertext_bytes = aes.encrypt_to_bytes(content_str)
    return ciphertext_bytes


def encrypt_to_base64(content_str, encrypt_key: str , iv : str) -> str:
    """From string encrypt to base64 ciphertext.
    """

    aes: AES_Turbe = AES_Turbe(encrypt_key,iv)
    ciphertext_bs64 = aes.encrypt_to_base64(content_str)
    return ciphertext_bs64


def decrypt_from_bytes(ciphertext_bytes, decrypt_key: str) -> str:
    """From bytes ciphertext decrypt to string.
    """

    aes: AES_Turbe = AES_Turbe(decrypt_key)
    content_str = aes.decrypt_from_bytes(ciphertext_bytes)
    return content_str


def decrypt_from_base64(ciphertext_bs64, decrypt_key: str , iv : str) -> str:
    """From base64 ciphertext decrypt to string.
    """

    aes: AES_Turbe = AES_Turbe(decrypt_key,iv)
    content_str = aes.decrypt_from_base64(ciphertext_bs64)
    return content_str


if __name__ == "__main__":
    key = "827d93f9-2e75-4842-a142-8813f31aaef9"
    iv = "t00349j083UC8Og7"
    #加密
    content = "fdtest"
    encrypt_msg = encrypt_to_base64(content,key,iv)
    print("encrypt_msg = " , encrypt_msg)


    #QRozfB7o+81cfg464xP34Q==  #正确加密后数据

    #YI/s3pHWwoivVo1xGwU5+w==


    #解密
    ct = "YI/s3pHWwoivVo1xGwU5+w=="
    ret = decrypt_from_base64(ct, key,iv)
    print("cet = " , ret)