import graphene
from graphene_federation import key,external,extend

from project_dtos.Enums import GenderEnum, ProfileTypeEnum
from project_dtos.Response import PageObject, ResponseObject
from project_dtos.Uaa_dto import UserRoleObjects

class UserInputObject(graphene.InputObjectType):
    profile_unique_id = graphene.String()
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    profile_phone = graphene.String()
    profile_photo = graphene.String()
    profile_gender = GenderEnum()
    profile_type = ProfileTypeEnum()


@key(fields='id')
class UserProfileObject(graphene.ObjectType):
    id = graphene.String()
    profile_unique_id = graphene.String()
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_email = graphene.String()
    profile_phone = graphene.String()
    profile_photo = graphene.String()
    profile_is_active = graphene.Boolean()
    profile_gender = GenderEnum()
    profile_type = ProfileTypeEnum()
    roles = graphene.Field(UserRoleObjects)
    

class ProfileResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileObject)
    # page = graphene.Field(PageObject)

class ProfileInputObject(graphene.InputObjectType):
    page_number = graphene.Int(required=True)


class UserFilteringInputObject(graphene.InputObjectType):   
    profile_gender = GenderEnum()
    profile_type = ProfileTypeEnum()
    profile_unique_id = graphene.String()
    profile_role_unique_id = graphene.String()

class UserProfileAndRoleObjects(graphene.ObjectType):
    id = graphene.String()
    user_profile = graphene.Field(UserProfileObject)
    user_roles = graphene.Field(UserRoleObjects)

class UserProfileAndRoleResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    page = graphene.Field(PageObject)
    data = graphene.List(UserProfileAndRoleObjects)

class UsersResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    page = graphene.Field(PageObject)
    data = graphene.List(UserProfileAndRoleObjects)


class SetPasswordInputObject(graphene.InputObjectType):
    request_token = graphene.String()
    user_password = graphene.String()
    confirm_password = graphene.String()

class ForgortPasswordInputObject(graphene.InputObjectType):
    old_password = graphene.String()
    new_password = graphene.String()

class ActivateDeactivateFilteringInputObject(graphene.InputObjectType):
    profile_unique_id = graphene.String()
    profile_is_active = graphene.Boolean()




