import sqlalchemy
import sqlalchemy.orm

from app import model
from app.services import utils


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


class SpeciesFilter:
    def __init__(
        self,
        taxon_orders: list[int] = None,
        chinese_common_name: str = None,
        english_common_name: str = None,
        scientific_name: str = None,
        name: str = None,
        conservation_status: str = None,
        orders: list[str] = None,
        families: list[str] = None,
        codes: list[str] = None,
    ) -> None:
        self.taxon_orders = taxon_orders
        self.chinese_common_name = chinese_common_name
        self.english_common_name = english_common_name
        self.scientific_name = scientific_name
        self.name = name
        self.conservation_status = conservation_status
        self.orders = orders
        self.families = families
        self.codes = codes

    def filter_query(
        self,
        query: sqlalchemy.orm.Query[model.Species],
    ) -> sqlalchemy.orm.Query[model.Species]:

        if self.taxon_orders:
            query = query.filter(model.Species.taxon_order.in_(self.taxon_orders))

        if self.chinese_common_name:
            chinese_name_search = utils.SearchStr(self.chinese_common_name)
            query = query.filter(
                model.Species.chinese_common_name.like(
                    chinese_name_search.search_phrase
                )
            )
        if self.english_common_name:
            english_name_search = utils.SearchStr(self.english_common_name)
            query = query.filter(
                model.Species.english_common_name.like(
                    english_name_search.search_phrase
                )
            )
        if self.scientific_name:
            scientific_name_search = utils.SearchStr(self.scientific_name)
            query = query.filter(
                model.Species.scientific_name.like(scientific_name_search.search_phrase)
            )

        if self.name:
            name_search = utils.SearchStr(self.name)
            query = query.filter(
                sqlalchemy.or_(
                    model.Species.chinese_common_name.like(name_search.search_phrase),
                    model.Species.english_common_name.like(name_search.search_phrase),
                    model.Species.scientific_name.like(name_search.search_phrase),
                )
            )
        if self.orders:
            query = query.filter(model.Species.order.in_(self.orders))
        if self.families:
            query = query.filter(
                sqlalchemy.or_(
                    model.Species.family_name.in_(self.families),
                    model.Species.family_latin_name.in_(self.families),
                )
            )
        if self.conservation_status:
            query = query.filter(
                model.Species.conservation_status == self.conservation_status.upper()
            )
        if self.codes:
            query = query.filter(model.Species.codes.contains(self.codes))

        return query


if __name__ == "__main__":
    s = SearchStr("test")
    str()
    print(s.search_phrase)
    print(s)
