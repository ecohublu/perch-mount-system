from app.services import db
import app.services.perchai.utils as services_utils
from app import model


def get_species() -> list[model.Species]:
    with db.session.begin() as session:
        species_list = session.query(model.Species).all()

    return species_list


def get_species_by_filter(filter: services_utils.SpeciesFilter) -> list[model.Species]:
    modifier = services_utils.SpeciesQueryModifier(filter)
    with db.session.begin() as session:
        query = session.query(model.Species)
        query = modifier.filter_query(query)
        species_list = query.all()

    return species_list


def get_species_by_taxon_orders(taxon_orders: list[int]) -> list[model.Species]:
    with db.session.begin() as session:
        species = (
            session.query(model.Species)
            .filter(model.Species.taxon_order.in_(taxon_orders))
            .all()
        )
    return species


def get_species_by_taxon_order(taxon_order: int) -> model.Species | None:
    with db.session.begin() as session:
        species = (
            session.query(model.Species)
            .filter(model.Species.taxon_order == taxon_order)
            .one()
        )
    return species
