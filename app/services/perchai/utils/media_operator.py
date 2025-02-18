from datetime import datetime
import uuid

from app.model import enums


class DetectedIndividual:
    def __init__(
        self,
        taxon_order_by_ai: int,
        box_xmin: float = None,
        box_xmax: float = None,
        box_ymin: float = None,
        box_ymax: float = None,
    ):
        self.taxon_order_by_ai = taxon_order_by_ai
        self.box_xmin = box_xmin
        self.box_xmax = box_xmax
        self.box_ymin = box_ymin
        self.box_ymax = box_ymax


class ReviewedIndividual:
    def __init__(
        self,
        taxon_order_by_human,
        box_xmin=None,
        box_xmax=None,
        box_ymin=None,
        box_ymax=None,
    ):
        self.taxon_order_by_human = taxon_order_by_human
        self.box_xmin = box_xmin
        self.box_xmax = box_xmax
        self.box_ymin = box_ymin
        self.box_ymax = box_ymax


class UploadedMedium:
    def __init__(
        self,
        id_: str,
        section_id: str,
        medium_datetime: str,
        medium_type: enums.MediaTypes,
        nas_path: str,
    ):
        self.id = uuid.UUID(id_)
        self.section_id = uuid.UUID(section_id)
        self.medium_datetime = datetime.fromisoformat(medium_datetime)
        self.medium_type = medium_type
        self.nas_path = nas_path


class DetectedMedium:
    def __init__(
        self,
        id_: str,
        detected_at: datetime,
        individuals: list[dict] = [],
    ):
        self.id = uuid.UUID(id_)
        self.detected_at: datetime = datetime.fromisoformat(detected_at)
        self.individuals: list[DetectedIndividual] = [
            DetectedIndividual(**individual) for individual in individuals
        ]

    @property
    def no_individual(self) -> bool:
        return len(self.individuals) == 0

    @property
    def has_individual(self) -> bool:
        return len(self.individuals) > 0

    def to_unchecked(self) -> bool:
        return self.no_individual

    def to_unreviewed(self) -> bool:
        return self.has_individual


class CheckedMedium:
    def __init__(
        self,
        id_: str,
        empty_cheked_at: str,
        empty_checked_id: str,
        has_individual: bool,
    ):
        self.id: uuid.UUID = uuid.UUID(id_)
        self.empty_checked_at: datetime = datetime.fromisoformat(empty_cheked_at)
        self.empty_checker_id: uuid.UUID = uuid.UUID(empty_checked_id)
        self.has_individual: bool = has_individual

    @property
    def no_individual(self) -> bool:
        return not self.has_individual

    def to_acciental(self) -> bool:
        return not self.has_individual

    def to_unreviewed(self) -> bool:
        return self.has_individual


class ReviewedMedium:
    def __init__(
        self,
        id_: str,
        reviewed_at: str,
        reviewer_id: str,
        featured_by_id: str | None = None,
        event_id: str | None = None,
        behavior_id: str | None = None,
        individuals: list[dict] = [],
    ):
        self.id: uuid.UUID = uuid.UUID(id_)
        self.reviewed_at: datetime = datetime.fromisoformat(reviewed_at)
        self.reviewer_id: uuid.UUID = uuid.UUID(reviewer_id)

        self.featured_by_id: uuid.UUID | None = (
            uuid.UUID(featured_by_id) if featured_by_id else None
        )
        self.event_id: uuid.UUID | None = (
            uuid.UUID(event_id) if featured_by_id else None
        )
        self.behavior_id: uuid.UUID | None = (
            uuid.UUID(behavior_id) if featured_by_id else None
        )
        self.individuals: list[ReviewedIndividual] = [
            ReviewedIndividual(**individual) for individual in individuals
        ]

    @property
    def no_individual(self) -> bool:
        return len(self.individuals) == 0

    @property
    def has_individual(self) -> bool:
        return len(self.individuals) > 0

    def to_acciental(self) -> bool:
        return self.no_individual

    def to_reviewed(self) -> bool:
        return self.has_individual


class UploadedMedia(list):
    def __init__(self, iterable: list[UploadedMedium] = None):
        if iterable is None:
            iterable = []
        super().__init__(iterable)


class DetectedMedia(list):
    def __init__(self, iterable: list[DetectedMedium] = None):
        if iterable is None:
            iterable = []
        super().__init__(iterable)

    @property
    def media_to_unchecked(self: list[DetectedMedium]) -> list[DetectedMedium]:
        return [medium for medium in self if medium.no_individual]

    @property
    def media_to_unreviewed(self: list[DetectedMedium]) -> list[DetectedMedium]:
        return [medium for medium in self if medium.has_individual]


class CheckedMedia(list):
    def __init__(self, iterable: list[CheckedMedium] = None):
        if iterable is None:
            iterable = []
        super().__init__(iterable)

    @property
    def media_to_accidenal(self: list[CheckedMedium]) -> list[DetectedMedium]:
        return [medium for medium in self if medium.no_individual]

    @property
    def media_to_unreviewed(self: list[CheckedMedium]) -> list[DetectedMedium]:
        return [medium for medium in self if medium.has_individual]


class ReviewedMedia(list):
    def __init__(self, iterable: list[ReviewedMedium] = None):
        if iterable is None:
            iterable = []
        super().__init__(iterable)

    @property
    def media_to_accidenal(self: list[ReviewedMedium]) -> list[DetectedMedium]:
        return [medium for medium in self if medium.no_individual]

    @property
    def media_to_reviewed(self: list[ReviewedMedium]) -> list[DetectedMedium]:
        return [medium for medium in self if medium.has_individual]
