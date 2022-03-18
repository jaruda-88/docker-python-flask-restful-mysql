import datetime

def get_dt_now_to_str(strFomat='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(strFomat)