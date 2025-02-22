from app.resources.perchai import species

ROUTES = [
    {
        # species
        "route": "species",
        "resources": [species.Species],
        "children": [
            {
                "route": "<int:taxon_order>",
                "resources": [species.ASpecies],
                "children": [],
            }
        ],
    },
]
