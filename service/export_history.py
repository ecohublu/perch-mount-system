import datetime
import service
from service import query_utils
from src import model


def get_export_histories_by_exportor(exportor: int) -> model.ExportHistory:
    with service.session.begin() as session:
        result = (
            session.query(model.ExportHistory)
            .filter(model.ExportHistory.exportor == exportor)
            .filter(model.ExportHistory.expire_time < datetime.datetime.now())
            .all()
        )
    return result


def add_export_history():
    return
