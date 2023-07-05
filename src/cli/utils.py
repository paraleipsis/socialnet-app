import secrets


def generate_secret_key():
    secret_key = secrets.token_hex(32)

    return secret_key
