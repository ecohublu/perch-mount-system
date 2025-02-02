import sqlalchemy
import sqlalchemy.orm
import uuid

from app import model
from app.model import enums
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


class PerchAIFilter:
    def _strs_to_uuids(self, ids: list[str]) -> list[uuid.UUID]:
        return list(map(uuid.UUID, ids))


class PerchMountFilter(PerchAIFilter):
    def __init__(
        self,
        project_ids: list[str] = None,
        claim_by_ids: list[str] = None,
        habitats: list[str] = None,
        terminated: bool = None,
    ) -> None:
        super().__init__()
        self.project_ids = self._strs_to_uuids(project_ids)
        self.claim_by_ids = self._strs_to_uuids(claim_by_ids)
        self.habitats = habitats
        self.terminated = terminated
        self._validate_enums()

    def filter_query(
        self, query: sqlalchemy.orm.Query
    ) -> sqlalchemy.orm.Query[model.PerchMounts]:

        if self.project_ids:
            query = query.filter(model.PerchMounts.project_id.in_(self.project_ids))

        if self.habitats:
            query = query.filter(model.PerchMounts.habitat.in_(self.habitats))

        if self.terminated is not None:
            query = query.filter(model.PerchMounts.terminated == self.terminated)

        if self.claim_by_ids:
            query = query.filter(model.PerchMounts.claim_by_id.in_(self.claim_by_ids))

        return query

    def _validate_enums(self):
        if self.habitats:
            enums.validate_enums(self.habitats, enum_type=enums.Habitats)


class SpeciesFilter(PerchAIFilter):
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
        super().__init__()
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
