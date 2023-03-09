import os
import asyncio
from concurrent.futures import ProcessPoolExecutor

from const import COOKIES_PATH, CACHE_DIR

async def multi_process(funcs):
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        tasks = []
        results = []
        for func in funcs:
            tasks.append(loop.run_in_executor(pool, func))
        for task in tasks:
            results.append(await task)
    return results

def isexists_login_info():
    return os.path.exists(COOKIES_PATH) and os.path.exists(os.path.join(CACHE_DIR, 'user-id.pkl'))