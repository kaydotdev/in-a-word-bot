import hmac
import hashlib


class PasswordHashGeneratingService:
    def __init__(self, secret):
        self.secret = secret

    def generate_password_hash(self, password):
        return hmac.new(bytes(self.secret, 'UTF-8'),
                        msg=bytes(password, 'UTF-8'),
                        digestmod=hashlib.sha256).hexdigest().upper()
