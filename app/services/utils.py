import sqlalchemy.orm
import uuid


class SearchStr(str):

    def __init__(self, string: str) -> None:
        super().__init__()
        self.string = string

    @property
    def search_phrase(self) -> str:
        return f"%{self.__str__()}%"

    @property
    def search_phrase_from_start(self) -> str:
        return f"{self.__str__()}%"

    @property
    def search_phrase_from_end(self) -> str:
        return f"%{self.__str__()}"


class QueryFilter:
    def __init__(self, offset: int = 0, limit: int = 50):
        self.offset = offset
        self.limit = limit

    def _strs_to_uuids(self, ids: list[str]) -> list[uuid.UUID]:
        return list(map(uuid.UUID, ids))

    def to_bool(self, arg) -> bool:
        pass


class QueryModifier:
    def __init__(self, filter: QueryFilter):
        self.filter = filter

    def offset_query(self, query: sqlalchemy.orm.Query) -> sqlalchemy.orm.Query:
        return query.offset(self.filter.offset)

    def limit_query(self, query: sqlalchemy.orm.Query) -> sqlalchemy.orm.Query:
        return query.limit(self.filter.limit)

    def _strs_to_uuids(self, ids: list[str]) -> list[uuid.UUID]:
        return list(map(uuid.UUID, ids))
