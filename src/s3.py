import urllib.parse
from minio import Minio
from src import config

URL = urllib.parse.urlparse(config.get_env(config.EnvKeys.MINIO))
ACCESS_KEY = config.get_env(config.EnvKeys.MINIO_ACCESS_KEY)
SECRET_KEY = config.get_env(config.EnvKeys.MINIO_SECRET_KEY)

client = Minio(
    URL.netloc,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False,
)
