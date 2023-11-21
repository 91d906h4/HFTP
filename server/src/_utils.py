# Import modules.
import datetime

def get_time() -> str:
    return str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))