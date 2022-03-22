import datetime
from pytz import timezone
import jwt


def get_dt_now(tz):
    return datetime.datetime.now(timezone(tz))


def get_add_hour_to_dt_now(value, tz='Asia/Seoul'):
    return get_dt_now(tz) + datetime.timedelta(hours=value)


def get_add_second_to_dt_now(value, tz='Asia/Seoul'):
    return get_dt_now(tz) + datetime.timedelta(seconds=value)


def get_dt_now_to_str(fomat='%Y-%m-%d %H:%M:%S', tz='Asia/Seoul'):
    return get_dt_now(tz).strftime(fomat)


def encode_token(payload):
    return jwt.encode(payload, 'project1', algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, 'project1', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
