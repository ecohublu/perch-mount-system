import sqlalchemy

from app.services import mainapi
from app.services import utils
from app import model


def get_species(
    taxon_orders: list[int] = None,
    chinese_name: str = None,
    english_name: str = None,
    scientific_name: str = None,
    name: str = None,
    orders: list[str] = None,
    families: list[str] = None,
    conservation_status: str = None,
    codes: list[str] = None,
) -> list[model.Species]:

    with mainapi.session.begin() as session:
        query = session.query(model.Species)
        if taxon_orders:
            query = query.filter(model.Species.taxon_order.in_(taxon_orders))

        if chinese_name:
            chinese_name_search = utils.SearchStr(chinese_name)
            query = query.filter(
                model.Species.chinese_common_name.like(
                    chinese_name_search.search_phrase
                )
            )
        if english_name:
            english_name_search = utils.SearchStr(english_name)
            query = query.filter(
                model.Species.english_common_name.like(
                    english_name_search.search_phrase
                )
            )
        if scientific_name:
            scientific_name_search = utils.SearchStr(scientific_name)
            query = query.filter(
                model.Species.scientific_name.like(scientific_name_search.search_phrase)
            )

        if name:
            name_search = utils.SearchStr(name)
            query = query.filter(
                sqlalchemy.or_(
                    model.Species.chinese_common_name.like(name_search.search_phrase),
                    model.Species.english_common_name.like(name_search.search_phrase),
                    model.Species.scientific_name.like(name_search.search_phrase),
                )
            )
        if orders:
            query = query.filter(model.Species.order.in_(orders))
        if families:
            query = query.filter(
                sqlalchemy.or_(
                    model.Species.family_name.in_(families),
                    model.Species.family_latin_name.in_(families),
                )
            )
        if conservation_status:
            query = query.filter(
                model.Species.conservation_status == conservation_status.upper()
            )
        if codes:
            query = query.filter(model.Species.codes.contains(codes))

        species_list = query.all()

    return species_list


def get_species_by_taxon_orders(taxon_orders: list[int]) -> list[model.Species]:
    with mainapi.session.begin() as session:
        species = (
            session.query(model.Species)
            .filter(model.Species.taxon_order.in_(taxon_orders))
            .all()
        )
    return species


def get_species_by_taxon_order(taxon_order: int) -> model.Species:
    with mainapi.session.begin() as session:
        species = (
            session.query(model.Species)
            .filter(model.Species.taxon_order == taxon_order)
            .one()
        )
    return species
