from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64, hashlib, os

class EncryptedPass:

    def hash(self, password):
        return hashlib.sha512(password.encode()).hexdigest()

    def salt(self):
        return base64.b64encode(os.urandom(60))

    def validate(self, password, salt, expectation):
        return self.hash(password + salt) == expectation
   
class Cipher:
    '''
    REF:
    https://nitratine.net/blog/post/encryption-and-decryption-in-python/

    Encrypts and decrypts api_key, api_secret, access_token, token_secret
    for Twitter application, based on the users password for this webapp
    (only the user knows their webapp password!)
    '''
    def __init__(self, password, salt):
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
                )
        self.key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
                
    def encrypt(self, data):
        return Fernet(self.key).encrypt(data.encode())

    def decrypt(self, data):
        return Fernet(self.key).decrypt(data).decode()
