from datetime import datetime

from app.model import enums
from app.services import utils as service_utils


class PerchMountFilter(service_utils.QueryFilter):
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
        self._validate_all_enums()

    def _validate_all_enums(self):
        if self.habitats:
            enums.validate_enums(self.habitats, enum_type=enums.Habitats)


class SectionFilter(service_utils.QueryFilter):
    def __init__(
        self,
        perch_mount_ids: list[str] = None,
        swapped_date_from: datetime = None,
        swapped_date_to: datetime = None,
        swapper_ids: list[str] = None,
    ) -> None:
        super().__init__()
        self.perch_mount_ids = self._strs_to_uuids(perch_mount_ids)
        self.swapped_date_from = swapped_date_from
        self.swapped_date_to = swapped_date_to
        self.swapper_ids = self._strs_to_uuids(swapper_ids)


class MediaFilter(service_utils.QueryFilter):
    def __init__(
        self,
        status: enums.MediaStatus,
        perch_mount_ids: list[str] = None,
        section_ids: list[str] = None,
        is_tagged: bool = None,
        ring_number_search: str = None,
        prey_status: str = None,
        has_prey: bool = None,
        prey_inaturalist_taxa_ids: list[int] = None,
        taxon_orders_by_human: list[int] = None,
        taxon_orders_by_ai: list[int] = None,
    ):
        super().__init__()
        self.status = status
        self.perch_mount_ids = self._strs_to_uuids(perch_mount_ids)
        self.section_ids = self._strs_to_uuids(section_ids)
        self.is_tagged = is_tagged
        self.ring_number_search = ring_number_search
        self.prey_status = prey_status
        self.has_prey = has_prey
        self.prey_inaturalist_taxa_ids = prey_inaturalist_taxa_ids
        self.taxon_orders_by_human = taxon_orders_by_human
        self.taxon_orders_by_ai = taxon_orders_by_ai


class SpeciesFilter(service_utils.QueryFilter):
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
