import jwt
import datetime
from jwt import exceptions

SALT = 'apple'

def create_token():
    # 构造header
    headers = {
    'typ': 'jwt',
    'alg': 'HS256'
    }
    # 构造payload
    payload = {
    'userid': 1, # 自定义用户ID
    'username': 'pig',
    'age':33,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50)
    }
    result = jwt.encode(payload=payload, key=SALT, algorithm='HS256', headers=headers).decode('utf8')
    return result

def parse_payload(token):
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, SALT)
        result['status'] = True
        result['data'] = verified_payload
        print(verified_payload)
    except exceptions.ExpiredSignatureError:
            result['error'] = 'token已失效'
    except jwt.DecodeError:
            result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
            result['error'] = '非法的token'
    return result
# eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InBpZyIsImV4cCI6MTU4MzYyNzI0MH0.q0y2hX1ZceK6xxaWcBIhN08-ugRNF1WM6Sf0qlzQh4M
if __name__ == '__main__':
    # token = create_token()
    # print(token)
    result = parse_payload('eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOjEsInVzZXJuYW1lIjoicGlnIiwiYWdlIjozMywiZXhwIjoxNTgzMjA3Njg0fQ.gCgkfkPZrM2QjrXPr7b0ILpBdVTYUzsNGKT_xSFWDt0')
    print(result)