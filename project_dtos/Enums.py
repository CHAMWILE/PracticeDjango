import enum
import graphene



class GenderTypeInum(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

GenderEnum = graphene.Enum.from_enum(GenderTypeInum)


class ProfileTypeInum(enum.Enum):
    ADMIN = "ADMIN"
    REGISTERED_USER = "REGISTERED_USER"
    MANAGEMENT = "MANAGEMENT"

ProfileTypeEnum = graphene.Enum.from_enum(ProfileTypeInum)


class TimeRangeInum(enum.Enum):
    TODAY  = "TODAY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY  = "YEARLY"

TimeRangeEnum = graphene.Enum.from_enum(TimeRangeInum)

