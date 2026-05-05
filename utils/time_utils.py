from datetime import datetime
from zoneinfo import ZoneInfo


BOGOTA_TZ = ZoneInfo("America/Bogota")


def ahora_bogota():
    """
    Retorna la fecha y hora actual en zona horaria America/Bogota.
    Formato compatible con SQLite: YYYY-MM-DD HH:MM:SS
    """
    return datetime.now(BOGOTA_TZ).strftime("%Y-%m-%d %H:%M:%S")


def fecha_hoy_bogota():
    """
    Retorna la fecha actual en America/Bogota.
    Formato: YYYY-MM-DD
    """
    return datetime.now(BOGOTA_TZ).strftime("%Y-%m-%d")