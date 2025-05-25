from datetime import datetime
import uuid

from app.model import enums
from app import model


class DetectedIndividual:
    def __init__(
        self,
        taxon_order_by_ai: int,
        box_xmin: float | None = None,
        box_xmax: float | None = None,
        box_ymin: float | None = None,
        box_ymax: float | None = None,
    ):
        self.taxon_order_by_ai = taxon_order_by_ai
        self.box_xmin = box_xmin
        self.box_xmax = box_xmax
        self.box_ymin = box_ymin
        self.box_ymax = box_ymax


class ReviewedIndividual:
    def __init__(
        self,
        taxon_order_by_human: int,
        has_prey: bool,
        is_tagged: bool,
        has_ring: bool,
        id: str | None = None,
        box_xmin: float | None = None,
        box_xmax: float | None = None,
        box_ymin: float | None = None,
        box_ymax: float | None = None,
        ring_number: str | None = None,
    ):
        self.id = id
        self.taxon_order_by_human = taxon_order_by_human
        self.box_xmin = box_xmin
        self.box_xmax = box_xmax
        self.box_ymin = box_ymin
        self.box_ymax = box_ymax
        self.has_prey = has_prey
        self.is_tagged = is_tagged
        self.has_ring = has_ring
        self.ring_number = ring_number

    @property
    def is_ai_detected(self) -> bool:
        return self.id is not None

    @property
    def is_to_marked_prey_contents(self) -> bool:
        return self.has_prey

    @property
    def is_to_tagged_contents(self) -> bool:
        return self.is_tagged

    def __str__(self):
        return (
            f"ReviewedIndividual(\n"
            f"  id={self.id},\n"
            f"  taxon_order_by_human={self.taxon_order_by_human},\n"
            f"  box_xmin={self.box_xmin},\n"
            f"  box_xmax={self.box_xmax},\n"
            f"  box_ymin={self.box_ymin},\n"
            f"  box_ymax={self.box_ymax},\n"
            f"  has_prey={self.has_prey},\n"
            f"  is_tagged={self.is_tagged},\n"
            f"  has_ring={self.has_ring},\n"
            f"  ring_number={self.ring_number},\n"
            f"  is_ai_detected={self.is_ai_detected},\n"
            f"  is_to_marked_prey_contents={self.is_to_marked_prey_contents},\n"
            f"  is_to_tagged_contents={self.is_to_tagged_contents}\n"
            f")"
        )


class UploadedMedium:
    def __init__(
        self,
        medium_datetime: str,
        medium_type: enums.MediaTypes,
        nas_path: str,
    ):
        self.medium_datetime = datetime.fromisoformat(medium_datetime)
        self.medium_type = medium_type
        self.nas_path = nas_path


class DetectedMedium:
    def __init__(
        self,
        id: str,
        detected_at: datetime,
        individuals: list[dict] = [],
    ):
        self.id = id
        self.detected_at = detected_at
        self.individuals: list[DetectedIndividual] = [
            DetectedIndividual(**individual) for individual in individuals
        ]

    @property
    def no_individual(self) -> bool:
        return len(self.individuals) == 0

    @property
    def has_individual(self) -> bool:
        return len(self.individuals) > 0

    def is_to_unchecked(self) -> bool:
        return self.no_individual

    def is_to_unreviewed(self) -> bool:
        return self.has_individual


class CheckedMedium:
    def __init__(
        self,
        id: uuid.UUID,
        empty_checked_at: datetime,
        empty_checker_id: uuid.UUID,
        has_individual: bool,
    ):
        self.id = id
        self.empty_checked_at = empty_checked_at
        self.empty_checker_id = empty_checker_id
        self.has_individual = has_individual

    @property
    def no_individual(self) -> bool:
        return not self.has_individual

    def is_to_acciental(self) -> bool:
        return not self.has_individual

    def is_to_unreviewed(self) -> bool:
        return self.has_individual


class ReviewedMedium:
    def __init__(
        self,
        id: str,
        reviewed_at: datetime,
        reviewer_id: str,
        featured_by_id: str | None = None,
        event_id: str | None = None,
        behavior_id: str | None = None,
        individuals: list[dict] = [],
    ):
        self.id = id
        self.reviewed_at = reviewed_at
        self.reviewer_id = reviewer_id
        self.featured_by_id = featured_by_id
        self.event_id = event_id
        self.behavior_id = behavior_id
        self.individuals: list[ReviewedIndividual] = [
            ReviewedIndividual(**individual) for individual in individuals
        ]

    @property
    def no_individual(self) -> bool:
        return len(self.individuals) == 0

    @property
    def has_individual(self) -> bool:
        return len(self.individuals) > 0

    def is_to_acciental(self) -> bool:
        return self.no_individual

    def is_to_reviewed(self) -> bool:
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
    def media_to_accidenal(self: list[ReviewedMedium]) -> list[ReviewedMedium]:
        return [medium for medium in self if medium.no_individual]

    @property
    def media_to_reviewed(self: list[ReviewedMedium]) -> list[ReviewedMedium]:
        return [medium for medium in self if medium.has_individual]


class _ReviewedNewIndividuals:
    def __init__(self, individuals: list[ReviewedIndividual]):
        self.model_sets = self._to_model_sets(individuals)

    def _to_model_sets(self, individuals: list[ReviewedIndividual]) -> list[
        tuple[
            model.Individuals,
            model.ReviewedIndividualsContents | None,
            model.MarkedPreyIndividualsContents | None,
            model.TaggedIndividualsContents | None,
        ]
    ]:
        sets = []
        for individual in individuals:
            sets.append((model.Individuals(medium_id=individual)))
        return
