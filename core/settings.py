from starlette.config import Config
config = Config(".env")

API_TOKEN = config("API_TOKEN", cast=str, default="")
DATA_FILE = config("DATA_FILE", cast=str, default="")
headers =  {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117'
    }