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


def check_token(headers):
    ''' jwt 복호화 후 token의 payload return '''
    try:
        auth = headers.get('Authorization')

        if auth is None:
            return HTTPStatus.NON_AUTHORITATIVE_INFORMATION, "None token"

        payload = decode_token(auth)

        if payload is None:
            return HTTPStatus.NOT_ACCEPTABLE, "Token Expiration"

        return HTTPStatus.OK, payload
    except Exception as ex:
        return HTTPStatus.INTERNAL_SERVER_ERROR, ex.args[0]
