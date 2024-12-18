import graphene
from graphene import ObjectType

from project_account.models import UsersProfiles
from project_dtoBuilder.UserAccountsBuilders import UserAccountBuilder
from project_dtos.Response import ResponseObject
from project_dtos.UserAccount import ProfileResponseObject, UserFilteringInputObject
from project_utils.UserUtils import UserUtils


class Query(ObjectType): 
    get_users = graphene.Field(ProfileResponseObject, filtering=UserFilteringInputObject())
    get_user_profile = graphene.Field(ProfileResponseObject)

    # @has_query_access(permissions=['can_view_all_users'])
    def resolve_get_users(self, info,filtering=None,**kwargs):
      
        all_users =UsersProfiles.objects.filter(profile_is_active=True).values('profile_unique_id','profile_type')
        
        if filtering is None:
            return info.return_type.graphene_type(response=ResponseObject.get_response(id="24"),data=None)

        if filtering.profile_type:
            all_users = all_users.filter(profile_type=filtering.profile_type.value)

        if filtering.profile_gender:
            all_users = all_users.filter(profile_gender=filtering.profile_gender.value)
            
        if filtering.profile_unique_id:
            all_users = all_users.filter(profile_unique_id=filtering.profile_unique_id)

        all_users_list = list(map(lambda x: UserAccountBuilder.get_user_profile_data(str(x['profile_unique_id'])), all_users))
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"),data=all_users_list)
    
    
    # @has_query_access(permissions=['can_view_my_profile'])
    def resolve_get_user_profile(self, info,  filtering= None, **kwargs):

        profile_unique_id = UserUtils.__profile__(info.context.headers)
        user_profile = UsersProfiles.objects.filter(profile_unique_id=profile_unique_id).first()

        # if filtering is None:
        #     return info.return_type.graphene_type(response=ResponseObject.get_response(id="24"), data=None)
        #
        # if filtering.profile_unique_id:
        #     user_profile = user_profile.filter(profile_unique_id=filtering.profile_unique_id.value)
        #
        # if filtering.profile_gender:
        #     user_profile = user_profile.filter(profile_unique_id=filtering.profile_gender.value)
        #
        # if filtering.profile_type:
        #     user_profile = user_profile.filter(profile_type=filtering.profile_type.value)
        #
        # if filtering.profile_role_unique_id:
        #     user_profile = user_profile.filter(profile_role_unique_id=filtering.profile_role_unique_id.value)

        user = UserAccountBuilder.get_user_profile_data(user_profile.profile_unique_id)
        return info.return_type.graphene_type(response=ResponseObject.get_response(id="1"),data=user)
