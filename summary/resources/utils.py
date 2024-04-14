from urllib import parse

from src import config


def get_export_data_url(filename: str) -> str:
    host = config.get_env(config.EnvKeys.MINIO_HTTPS_HOST)
    bucket = config.get_env(config.EnvKeys.MINIO_DATA_EXPORT_BUCKET)

    return parse.urljoin(host, f"{bucket}/{filename}")
