from app.services import perchai
from app.services.perchai.utils import query_filter, query_modifier
from app import model


def get_species() -> list[model.Species]:
    with perchai.session.begin() as session:
        species_list = session.query(model.Species).all()

    return species_list


def get_species_by_filter(filter: query_filter.SpeciesFilter) -> list[model.Species]:
    modifier = query_modifier.SpeciesQueryModifier(filter)
    with perchai.session.begin() as session:
        query = session.query(model.Species)
        query = modifier.filter_query(query)
        species_list = query.all()

    return species_list


def get_species_by_taxon_orders(taxon_orders: list[int]) -> list[model.Species]:
    with perchai.session.begin() as session:
        species = (
            session.query(model.Species)
            .filter(model.Species.taxon_order.in_(taxon_orders))
            .all()
        )
    return species


def get_species_by_taxon_order(taxon_order: int) -> model.Species:
    with perchai.session.begin() as session:
        species = (
            session.query(model.Species)
            .filter(model.Species.taxon_order == taxon_order)
            .one()
        )
    return species
