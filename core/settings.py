from starlette.config import Config
config = Config(".env")

LOGIN = config("LOGIN", cast=str, default="")
PASSWORD = config("PASSWORD", cast=str, default="")
headers =  {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117'
    }