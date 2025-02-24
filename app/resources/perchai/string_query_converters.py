from app.resources import utils
from datetime import datetime

species = utils.StringQueryTypeCoverter(
    {
        "taxon_orders": utils.StringQueryTypeCoverter.to_int_list,
        "chinese_common_name": str,
        "english_common_name": str,
        "scientific_name": str,
        "name": str,
        "conservation_status": str,
        "protected": utils.StringQueryTypeCoverter.to_bool,
        "orders": utils.StringQueryTypeCoverter.to_str_list,
        "families": utils.StringQueryTypeCoverter.to_str_list,
        "codes": utils.StringQueryTypeCoverter.to_str_list,
    }
)

section = utils.StringQueryTypeCoverter(
    {
        "perch_mount_ids": utils.StringQueryTypeCoverter.to_uuid_list,
        "swapped_date_from": datetime.fromisoformat,
        "swapped_date_to": datetime.fromisoformat,
        "swapper_ids": utils.StringQueryTypeCoverter.to_uuid_list,
    }
)

perch_mount = utils.StringQueryTypeCoverter(
    {
        "project_ids": utils.StringQueryTypeCoverter.to_uuid_list,
        "claim_by_ids": utils.StringQueryTypeCoverter.to_uuid_list,
        "habitats": utils.StringQueryTypeCoverter.to_str_list,
        "terminated": utils.StringQueryTypeCoverter.to_bool,
    }
)
