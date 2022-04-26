import datetime
from pytz import timezone
import jwt
import hashlib
from http import HTTPStatus


def get_dt_now(tz):
    return datetime.datetime.now(timezone(tz))


def get_add_hour_to_dt_now(value, tz='Asia/Seoul'):
    return get_dt_now(tz) + datetime.timedelta(hours=value)


def get_add_second_to_dt_now(value, tz='Asia/Seoul'):
    return get_dt_now(tz) + datetime.timedelta(seconds=value)


def get_dt_now_to_str(fomat='%Y-%m-%d %H:%M:%S', tz='Asia/Seoul'):
    return get_dt_now(tz).strftime(fomat)


def get_password_sha256_hash(pw):
    ''' 비밀번호 sha256 암호화 '''
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()


def encode_token(payload):
    ''' jwt 암호화 '''
    return jwt.encode(payload, 'project1', algorithm='HS256')


def decode_token(token):
    ''' jwt 복호화 '''
    try:
        return jwt.decode(token, 'project1', algorithms=['HS256'])
    # token 유효시간 만료 에러
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def check_token(headers):
    ''' jwt 복호화 후 token의 payload return '''
    try:
        auth = headers.get('Authorization')

        if auth is None:
            return HTTPStatus.NON_AUTHORITATIVE_INFORMATION, "None token"

        payload = decode_token(auth)

        if payload is None:
            return HTTPStatus.UNAUTHORIZED, "Token Expiration or error value"

        return HTTPStatus.OK, payload
    except Exception as ex:
        return HTTPStatus.INTERNAL_SERVER_ERROR, ex.args[0]


def is_token(headers):
    ''' jwt 복호화 후 token의 payload return '''
    try:
        auth = headers.get('Authorization')

        if auth is None:
            raise Exception("None token")

        try:
            payload = jwt.decode(auth, 'project1', algorithms=['HS256'])
        # token 유효시간 만료 에러
        except jwt.ExpiredSignatureError:
            raise Exception("Token Expiration")
        except jwt.InvalidTokenError:
            raise Exception("Token value error")
        else:
            return payload
    except Exception as ex:
        raise Exception(ex.args[0])


def is_blank_str(string : str):
    """ 문자열 공백 체크 공백이면 True 아니면 False """
    return not (string and string.strip())


def check_body_request(req, args):
    """ api request body 유효성 확인 args tuple or str """
    if req is None:
        return HTTPStatus.NO_CONTENT, "Request data is empty"

    if type(args) is tuple:
        for key in args:
            if key == 'id':
                if int(req[key]) <= 0:
                    return HTTPStatus.NOT_FOUND, f'No value {key}'
            else:
                if is_blank_str(req[key]):
                    return HTTPStatus.NOT_FOUND, f'No value {key}'
    elif is_blank_str(req[args]):
        return HTTPStatus.NOT_FOUND, f'No value {key}'
    
    return HTTPStatus.OK, 'Ok'

        
