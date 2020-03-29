

from django.utils.timezone import now as djnow
from django.utils.timezone import datetime, timedelta

import json

def now():
    return djnow()

def is_json(s):
    try:
        json.loads(s)
        return True
    except:
        return False

def str2json(s):
    if is_json(s):
        return json.loads(s)
    else:
        return ''
