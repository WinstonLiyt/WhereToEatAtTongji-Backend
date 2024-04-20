import jwt
import datetime

from django.conf import settings

# 需要传入
def create_token(payload, timeout=1):
    salt = settings.SECRET_KEY

    # 构造header
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    
    # 其实就是往payload加入了有效时间
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)  # 有效时间

    token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers)
    return token
