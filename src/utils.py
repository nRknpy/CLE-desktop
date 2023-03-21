import os
import unicodedata
import asyncio
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

from const import COOKIES_PATH, CACHE_DIR


def isexists_login_info():
    return os.path.exists(COOKIES_PATH) and os.path.exists(os.path.join(CACHE_DIR, 'user-id.pkl'))


def dbstrlen(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


def now_second():
    dt = datetime.now()
    s = dt.second
    ms = dt.microsecond * 1e-6
    return s + ms
