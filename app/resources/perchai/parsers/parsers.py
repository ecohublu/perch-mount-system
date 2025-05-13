from app.resources.utils import parser
from app.resources.perchai.parsers import (
    media_oper_schema,
    prey_oper_schema,
    schemas,
)


class Species(parser.Parser):
    get = schemas.SpeciesGetSchema()


class Sections(parser.Parser):
    get = schemas.SectionsGetSchema()

    post = schemas.SectionPostSchema()


class Section(parser.Parser):
    patch = schemas.SectionPatchSchema()


class SectionSwappers(parser.Parser):
    put = schemas.SectionSwappersPutSchema()


class SectionTime(parser.Parser):
    patch = schemas.SectionTimePatchSchema()


class PerchMounts(parser.Parser):
    get = schemas.PerchMountsGetSchema()

    post = schemas.PerchMountsPostSchema()


class PerchMount(parser.Parser):
    patch = schemas.PerchMountPatchSchema()


class PerchMountClaimBy(parser.Parser):
    post = schemas.PerchMountClaimByPostSchema()


class Media(parser.Parser):
    get = schemas.MediaGetSchema()


class Medium(parser.Parser):
    patch = schemas.MediumPatchSchema()


class MediumStatus(parser.Parser):
    patch = schemas.MediumStatusPatchSchema()


class MediumFeature(parser.Parser):
    patch = schemas.MediumFeaturePatchSchema()


class Individual(parser.Parser):
    patch = schemas.IndividualPatchSchema()


class IndividualPrey(parser.Parser):
    post = schemas.IndividualPreyPostSchema()
    patch = schemas.IndividualPreyPatchSchema()


class IdentifiedPreys(parser.Parser):
    post = prey_oper_schema.IdentifiedPreySchema(many=True)


class IndividualNote(parser.Parser):
    put = schemas.IndividualNotePutSchema()


class UploadedMedia(parser.Parser):
    post = media_oper_schema.UploadedMediumSchema(many=True)


class DetectedMedia(parser.Parser):
    post = media_oper_schema.DetectedMediumSchema(many=True)


class CheckedMedia(parser.Parser):
    post = media_oper_schema.CheckedMediumSchema(many=True)


class ReviewedMedia(parser.Parser):
    post = media_oper_schema.ReviewedMediumSchema(many=True)


class Member(parser.Parser):
    patch = schemas.MemberPatchSchema()


class Members(parser.Parser):
    post = schemas.MembersPostSchema()


class Project(parser.Parser):
    patch = schemas.ProjectPatchSchema()


class Projects(parser.Parser):
    post = schemas.ProjectsPostSchema()


class Cameras(parser.Parser):
    post = schemas.CamerasPostSchema()


class Events(parser.Parser):
    post = schemas.EventsPostSchema()


class MountTypes(parser.Parser):
    post = schemas.MountTypesPostSchema()


class Behaviors(parser.Parser):
    post = schemas.BehaviorsPostSchema()


class Contributions(parser.Parser):
    get = schemas.ContributionsGetSchema()


class MemberContributions(parser.Parser):
    get = schemas.MemberContributionsGetSchema()
