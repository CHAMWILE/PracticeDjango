import base64
import graphene
from graphene import ObjectType

from project_dtoBuilder.UAABuilder import UAABuilder
from project_dtos.Response import ResponseObject
from project_dtos.Uaa_dto import GroupedPermissionsResponseObject, PermisionFilteringInputObjects, UserRoleResponseObject, UserRolesFilteringInputObjects
from project_uaa.models import UserPermissionsGroup, UserRoles, UsersWithRoles
from project_utils.UserUtils import UserUtils


class Query(ObjectType): 
    get_roles = graphene.Field(UserRoleResponseObject,filtering=UserRolesFilteringInputObjects())
    get_system_permissions = graphene.Field(GroupedPermissionsResponseObject,filtering=PermisionFilteringInputObjects())
    get_current_user_roles = graphene.Field(UserRoleResponseObject)

    # @has_query_access(permissions=['can_view_system_settings_details'])
    def resolve_get_roles(self, info,filtering=None,**kwargs):
        try:

            roles=UserRoles.objects.filter(role_is_active=True).all()

            if filtering.role_unique_id is not None:
                roles=roles.filter(role_unique_id=filtering.role_unique_id).all()

            # else:
            #     roles=roles.filter(role_is_system_default=False).all()

            roles_list=[]
            for role in roles:
                roles_list.append(UAABuilder.get_role_data(role.role_unique_id))

            print('-------------------------')
            print(roles_list)

            return UserRoleResponseObject(response=ResponseObject.get_response(id="1"),data=roles_list)
        except Exception as e:
            print(e)
            return UserRoleResponseObject(response=ResponseObject.get_response(id="5"))
        

    # @has_query_access(permissions=['can_view_system_settings_details'])
    def resolve_get_system_permissions(self, info,filtering=None,**kwargs):
        try:
            permision_groups=UserPermissionsGroup.objects.filter(permission_group_is_global=False).all()
            
               
            if filtering is None:
                return info.return_type.graphene_type(response=ResponseObject.get_response(id="24"),data=None)
            
            if filtering.group_is_global is not None:
                permision_groups=permision_groups.filter(permission_group_is_global=filtering.group_is_global).all()
            
            if filtering.permission_group_unique_id is not None :
                permision_groups=permision_groups.filter(permission_group_unique_id=filtering.permission_group_unique_id).all()    
            
            permision_group_list=[]
            for permision_group in permision_groups:
                permision_group_list.append(UAABuilder.get_group_permissions_data(permision_group.permission_group_unique_id))
            
            return GroupedPermissionsResponseObject(response=ResponseObject.get_response(id="1"),data=permision_group_list)
        except:
            return GroupedPermissionsResponseObject(response=ResponseObject.get_response(id="5"))
    

    # @has_query_access(permissions=['can_manage_settings'])
    def resolve_get_current_user_roles(self, info,**kwargs):
        
        user_id = UserUtils.get_user(info.context.headers)['id']
        
        roles=UsersWithRoles.objects.filter(user_with_role_user_id=user_id).only('user_with_role_role__role_unique_id')
        
        roles_list=[]
        for role in roles:
            roles_list.append(UAABuilder.get_role_data(role.user_with_role_role.role_unique_id))
            
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"),data=roles_list)
       
   