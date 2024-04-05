import datetime
import service
import typing


_TAXON_ORDER_TYPE_OPTIONS = typing.Literal["ai", "human", "both"]


def get_export_data(
    project_ids: list[int] = [],
    perch_mount_ids: list[int] = [],
    section_ids: list[int] = [],
    start_time: datetime.datetime = None,
    end_time: datetime.datetime = None,
    prey: bool = None,
    prey_name: str = None,
    taxon_orders: list[int] = [],
    taxon_order_status: _TAXON_ORDER_TYPE_OPTIONS = "human",
):
    return
