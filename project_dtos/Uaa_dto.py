import graphene

from project_dtos.Response import ResponseObject, PageObject

class UserPermissionInputObjects(graphene.InputObjectType):
    group = graphene.String()
    name = graphene.String()
    code = graphene.String()

class UserPermisionObjects(graphene.ObjectType):
    id = graphene.String()
    permission_unique_id = graphene.String()
    permission_name = graphene.String()
    permission_code = graphene.String()


class PermisionFilteringInputObjects(graphene.InputObjectType):
    group_is_global = graphene.Boolean()
    permission_group_unique_id = graphene.String()

class RolePermissionsInput(graphene.InputObjectType):
    pass

class UserRolesInputObjects(graphene.InputObjectType):
    role_unique_id = graphene.String()
    role_name = graphene.String()
    role_description = graphene.String()
    role_permissions = graphene.List(graphene.String)

class UserRoleObjects(graphene.ObjectType):
    id = graphene.String()
    role_unique_id = graphene.String()
    role_name = graphene.String()
    role_description = graphene.String()
    role_permissions = graphene.List(graphene.String)


class UserRoleResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.List(UserRoleObjects)
    page = graphene.Field(PageObject)


class UserRolesFilteringInputObjects(graphene.InputObjectType):
    page_number = graphene.Int(required=True)
    role_unique_id = graphene.String()


class GroupedPermissionsObjects(graphene.ObjectType):
    id = graphene.String()
    permission_group_unique_id = graphene.String()
    permission_group_name = graphene.String()
    permission_group_is_global = graphene.Boolean()
    permissions = graphene.List(UserPermisionObjects)


class GroupedPermissionsResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.List(GroupedPermissionsObjects)



class UserPermissionMatrixResponseObject(graphene.ObjectType):
    response = graphene.Field(ResponseObject)
    data = graphene.String()


class UserHandoverInputObjects(graphene.InputObjectType):
    handover_receiver = graphene.String()
    handover_user = graphene.String()
    handover_onbehalf = graphene.Boolean()