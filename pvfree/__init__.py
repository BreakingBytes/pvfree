import os
import base64

DIRNAME = os.path.dirname(os.path.dirname(__file__))


def get_secret(key, filename=None, is_b64=True):
    """
    Read secret from environment variable or encrypted data from file.
    """
    secret = os.environ.get(key)
    if secret is None:
        if filename is None:
            raise KeyError(key)
        with open(os.path.join(DIRNAME, filename), 'rb') as fobj:
            secret = fobj.read()
        if is_b64:
            secret = base64.b64decode(secret)
    return secret
