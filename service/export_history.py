import datetime
import service
from src import model
from src import config


def get_export_histories_by_exportor(exportor: int = None) -> list[model.ExportHistory]:
    if not exportor:
        return []
    with service.session.begin() as session:
        result = (
            session.query(model.ExportHistory)
            .filter(model.ExportHistory.exportor == exportor)
            .filter(model.ExportHistory.expire_time > datetime.datetime.now())
            .all()
        )
    return result


def add_export_history(
    exportor: int,
    file_name: str,
):

    now = datetime.datetime.now()
    days = int(config.get_env(config.EnvKeys.EXPORT_DATA_RETAIN_DAYS))
    retain = datetime.timedelta(days=days)
    new_export_history = model.ExportHistory(
        exportor=exportor,
        file_name=file_name,
        expire_time=now + retain,
    )
    with service.session.begin() as session:
        session.add(new_export_history)
        session.commit()
    return new_export_history
