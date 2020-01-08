import hmac
import hashlib
import base64


class PasswordHashGeneratingService:
    def __init__(self, secret):
        self.secret = secret

    def generate_password_hash(self, password):
        return base64.b64encode(hmac.new(bytes(self.secret, 'UTF-8'),
                                         msg=bytes(password, 'UTF-8'),
                                         digestmod=hashlib.sha256).digest())
