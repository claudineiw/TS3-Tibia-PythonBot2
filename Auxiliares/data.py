import time
from datetime import datetime

import pytz


def utc_to_local(dt):
    local_timezone = pytz.timezone("America/Sao_Paulo")
    local_datetime = dt.replace(tzinfo=pytz.utc)
    local_datetime = local_datetime.astimezone(local_timezone)
    return time.strftime("%d/%m/%Y %H:%M:%S", local_datetime.timetuple())


def geHoraAtual(dataMorte):
    # local_timezone = pytz.timezone("America/Sao_Paulo")
    morte = datetime.strptime(dataMorte, "%d/%m/%Y %H:%M:%S")  # your date
    result = int((datetime.now() - morte).total_seconds()) / 60
    return result
