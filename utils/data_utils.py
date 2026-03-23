from datetime import datetime
import pytz

def agora():
    return datetime.now(pytz.timezone("America/Manaus"))

def hoje_str():
    return agora().strftime("%Y-%m-%d")

def hoje_formatado():
    return agora().strftime("%d/%m/%Y")