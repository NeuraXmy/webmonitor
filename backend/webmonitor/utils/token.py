from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app


def generate_token(data):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps(data)


def verify_token(token_str, expiration):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        return s.loads(token_str, max_age=expiration)
    except:
        return None