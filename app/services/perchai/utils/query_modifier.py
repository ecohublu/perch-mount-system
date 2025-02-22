import sqlalchemy
import sqlalchemy.orm

from app import model
from app.services.perchai.utils import query_filter
from app.services import utils as service_utils
from app.model import enums


class PerchMountQueryModifier(service_utils.QueryModifier):
    def __init__(self, filter: query_filter.PerchMountFilter) -> None:
        self.filter = filter
        super().__init__(filter)

    def filter_query(
        self, query: sqlalchemy.orm.Query
    ) -> sqlalchemy.orm.Query[model.PerchMounts]:

        if self.filter.project_ids:
            query = query.filter(
                model.PerchMounts.project_id.in_(self.filter.project_ids)
            )

        if self.filter.habitats:
            query = query.filter(model.PerchMounts.habitat.in_(self.filter.habitats))

        if self.filter.terminated is not None:
            query = query.filter(model.PerchMounts.terminated == self.filter.terminated)

        if self.filter.claim_by_ids:
            query = query.filter(
                model.PerchMounts.claim_by_id.in_(self.filter.claim_by_ids)
            )

        return query


class SectionQueryModifier(service_utils.QueryModifier):
    def __init__(self, filter: query_filter.SectionFilter) -> None:
        self.filter = filter
        super().__init__(filter)

    def filter_query(
        self, query: sqlalchemy.orm.Query
    ) -> sqlalchemy.orm.Query[model.Sections]:
        if self.filter.perch_mount_ids:
            query = query.filter(
                model.Sections.perch_mount_id.in_(self.filter.perch_mount_ids)
            )

        if self.filter.swapped_date_from:
            query = query.filter(
                model.Sections.swapped_date >= self.filter.swapped_date_from
            )

        if self.filter.swapped_date_to:
            query = query.filter(
                model.Sections.swapped_date < self.filter.swapped_date_to
            )

        if self.filter.swapper_ids:
            query = query.filter(
                model.Sections.swappers.any(
                    model.Members.id.in_(self.filter.swapper_ids)
                )
            )

        return query


class MediaQueryModifier(service_utils.QueryModifier):
    _BASIC_FIELDS = (
        model.Media.id,
        model.Media.section_id,
        model.Media.medium_datetime,
        model.Media.medium_type,
        model.Media.nas_path,
        model.Media.status,
        model.Media.section,
        # model.Media.individuals,
        # model.Media.unchecked_contents,
        # model.Media.detected_contents,
        # model.Media.checked_contents,
        # model.Media.reviewed_contents,
    )

    def __init__(self, filter: query_filter.MediaFilter):
        super().__init__(filter)
        self.filter = filter

    @property
    def fields(self) -> tuple:
        return self._BASIC_FIELDS

    def options(self, query: sqlalchemy.orm.Query[model.Media]) -> sqlalchemy.orm.Query:
        query = (
            query.options(sqlalchemy.orm.joinedload(model.Media.individuals))
            .options(sqlalchemy.orm.joinedload(model.Media.unchecked_contents))
            .options(sqlalchemy.orm.joinedload(model.Media.detected_contents))
            .options(sqlalchemy.orm.joinedload(model.Media.checked_contents))
            .options(sqlalchemy.orm.joinedload(model.Media.unreviewued_contents))
            .options(sqlalchemy.orm.joinedload(model.Media.reviewed_contents))
        )
        return query

    def filter_query(
        self, query: sqlalchemy.orm.Query[model.Media]
    ) -> sqlalchemy.orm.Query:
        query = query.filter(model.Media.status == self.filter.status.upper())
        if self.filter.perch_mount_ids:
            query = query.filter(
                model.Media.section.any(
                    model.Sections.perch_mount_id.in_(self.filter.perch_mount_ids)
                )
            )
        if self.filter.section_ids:
            query = query.filter(model.Media.section_id.in_(self.filter.section_ids))

        if self.filter.is_tagged is not None:
            query = query.filter(
                model.Media.individuals.any(
                    model.Individuals.tagged_contents.any(
                        model.TaggedIndividualsContents.is_tagged
                        == self.filter.is_tagged
                    )
                )
            )
        if self.filter.ring_number_search:
            ring_number_search = service_utils.SearchStr(self.filter.ring_number_search)
            query = query.filter(
                model.Media.individuals.any(
                    model.Individuals.tagged_contents.any(
                        model.TaggedIndividualsContents.ring_number.ilike(
                            ring_number_search.search_phrase
                        )
                    )
                )
            )

        if self.filter.prey_status:
            query = query.filter(
                model.Media.individuals.any(
                    model.Individuals.prey_status == self.filter.prey_status
                )
            )

        if self.filter.has_prey is not None:
            query = query.filter(
                model.Media.individuals.any(
                    model.Individuals.marked_prey_contents.any(
                        model.MarkedPreyIndividualsContents.has_prey
                        == self.filter.has_prey
                    )
                )
            )

        if self.filter.prey_inaturalist_taxa_ids:
            query = query.filter(
                model.Media.individuals.any(
                    model.Individuals.marked_prey_contents.any(
                        model.IdentifiedPreyIndividualsContents.inaturalist_taxa_id
                        == self.filter.prey_inaturalist_taxa_ids
                    )
                )
            )
            query = query.filter(
                model.IdentifiedPreyIndividualsContents.inaturalist_taxa_id.in_(
                    self.filter.prey_inaturalist_taxa_ids
                )
            )
        if self.filter.taxon_orders_by_human:
            query = query.filter(
                model.Media.individuals.any(
                    model.Individuals.marked_prey_contents.any(
                        model.ReviewedIndividualsContents.taxon_order_by_human.in_(
                            self.filter.taxon_orders_by_human
                        )
                    )
                )
            )

        if self.filter.taxon_orders_by_ai:
            query = query.filter(
                model.Media.individuals.any(
                    model.Individuals.marked_prey_contents.any(
                        model.UnreviewedIndividualsContents.taxon_order_by_ai.in_(
                            self.filter.taxon_orders_by_ai
                        )
                    )
                )
            )

        return query


class SpeciesQueryModifier(service_utils.QueryModifier):
    def __init__(self, filter: query_filter.SpeciesFilter) -> None:
        super().__init__(filter)
        self.filter = filter

    def filter_query(
        self,
        query: sqlalchemy.orm.Query[model.Species],
    ) -> sqlalchemy.orm.Query[model.Species]:

        if self.filter.taxon_orders:
            query = query.filter(
                model.Species.taxon_order.in_(self.filter.taxon_orders)
            )

        if self.filter.chinese_common_name:
            chinese_name_search = service_utils.SearchStr(
                self.filter.chinese_common_name
            )
            query = query.filter(
                model.Species.chinese_common_name.ilike(
                    chinese_name_search.search_phrase
                )
            )
        if self.filter.english_common_name:
            english_name_search = service_utils.SearchStr(
                self.filter.english_common_name
            )
            query = query.filter(
                model.Species.english_common_name.ilike(
                    english_name_search.search_phrase
                )
            )
        if self.filter.scientific_name:
            scientific_name_search = service_utils.SearchStr(
                self.filter.scientific_name
            )
            query = query.filter(
                model.Species.scientific_name.ilike(
                    scientific_name_search.search_phrase
                )
            )

        if self.filter.name:
            name_search = service_utils.SearchStr(self.filter.name)
            query = query.filter(
                sqlalchemy.or_(
                    model.Species.chinese_common_name.ilike(name_search.search_phrase),
                    model.Species.english_common_name.ilike(name_search.search_phrase),
                    model.Species.scientific_name.ilike(name_search.search_phrase),
                )
            )
        if self.filter.orders:
            query = query.filter(model.Species.order.in_(self.filter.orders))
        if self.filter.families:
            query = query.filter(
                sqlalchemy.or_(
                    model.Species.family_name.in_(self.filter.families),
                    model.Species.family_latin_name.in_(self.filter.families),
                )
            )
        if self.filter.conservation_status:
            query = query.filter(
                model.Species.conservation_status
                == self.filter.conservation_status.upper()
            )
        if self.filter.codes:
            upper_codes = [code.upper() for code in self.filter.codes]
            query = query.filter(model.Species.codes.overlap(upper_codes))

        return query
