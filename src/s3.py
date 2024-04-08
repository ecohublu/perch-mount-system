import urllib.parse
from minio import Minio
from src import config

URL = urllib.parse.urlparse(config.get_env(config.EnvKeys.MINIO))


client = Minio(
    URL.netloc,
    access_key=config.get_env(config.EnvKeys.MINIO_ACCESS_KEY),
    secret_key=config.get_env(config.EnvKeys.MINIO_SECRET_KEY),
    secure=False,
)
