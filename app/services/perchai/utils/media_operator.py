from datetime import datetime
import uuid


class DetectedIndividual:
    def __init__(self, json_individual: dict):
        self.taxon_order_by_ai = json_individual["taxon_order_by_ai"]
        self.box_xmin = json_individual["box_xmin"]
        self.box_xmax = json_individual["box_xmax"]
        self.box_ymin = json_individual["box_ymin"]
        self.box_ymax = json_individual["box_ymax"]


class ReviewedIndividual:
    def __init__(self, json_individual: dict):
        self.taxon_order_by_human = json_individual["taxon_order_by_ai"]
        self.box_xmin = json_individual["box_xmin"]
        self.box_xmax = json_individual["box_xmax"]
        self.box_ymin = json_individual["box_ymin"]
        self.box_ymax = json_individual["box_ymax"]


class DetectedMedium:
    def __init__(self, json_medium: dict):
        self.id: uuid.UUID = uuid.UUID(json_medium["id"])
        self.detected_at: datetime = datetime.fromisoformat(json_medium["detected_at"])
        self.individuals: list[DetectedIndividual] = list(
            map(DetectedIndividual, json_medium["individuals"])
        )

    @property
    def individuals_detected(self) -> bool:
        return len(self.individuals) > 0


class CheckedMedium:
    def __init__(self, json_medium: dict):
        self.id: uuid.UUID = uuid.UUID(json_medium["id"])
        self.empty_checked_at: datetime = datetime.fromisoformat(
            json_medium["empty_checked_at"]
        )
        self.empty_checker_id: uuid.UUID = uuid.UUID(json_medium["empty_checker_id"])
        self.with_individual: bool = json_medium["with_individual"]


class ReviewedMedium:
    def __init__(self, json_medium: dict):
        self.id: uuid.UUID = uuid.UUID(json_medium["id"])
        self.reviewed_at: datetime = datetime.fromisoformat(json_medium["reviewed_at"])
        self.reviewer_id: uuid.UUID = uuid.UUID(json_medium["reviewer_id"])
        self.fearured_by_id: uuid.UUID = uuid.UUID(json_medium["fearured_by_id"])
        self.event_id: uuid.UUID = uuid.UUID(json_medium["event_id"])
        self.behavior_id: uuid.UUID = uuid.UUID(json_medium["behavior_id"])
        self.individuals: list[ReviewedIndividual] = list(
            map(ReviewedIndividual, json_medium["individuals"])
        )

    @property
    def individuals_reviewed(self) -> bool:
        return len(self.individuals) > 0
