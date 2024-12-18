from project_account.models import UsersProfiles
from project_dtoBuilder.UAABuilder import UAABuilder
from project_dtos.Uaa_dto import UserRoleObjects
from project_dtos.UserAccount import UserProfileAndRoleObjects, UserProfileObject
from project_uaa.models import UsersWithRoles


class UserAccountBuilder:
    def get_user_profile_data(id):

            user_profile=UsersProfiles.objects.filter(profile_unique_id=id, profile_is_active=True).first()
            role=UsersWithRoles.objects.select_related("user_with_role_role").filter(user_with_role_user=user_profile.profile_user).first()
            return UserProfileObject(
                id = user_profile.primary_key,
                profile_unique_id = user_profile.profile_unique_id,
                user_first_name = user_profile.profile_user.first_name,
                user_last_name = user_profile.profile_user.last_name,
                user_email = user_profile.profile_user.email,
                profile_phone = user_profile.profile_phone,
                profile_photo = user_profile.profile_photo,
                profile_is_active = user_profile.profile_is_active,
                profile_type = user_profile.profile_type,
                profile_gender = user_profile.profile_gender,
                roles = UAABuilder.get_role_data(role.user_with_role_role.role_unique_id) if role else UserRoleObjects(),
            )
        
         
            
    def get_user_profile_and_role_data(id):
        
            user_profile=UsersProfiles.objects.filter(profile_is_active=True,profile_unique_id=id).first()
            user_with_role= UsersWithRoles.objects.filter(user_with_role_user=user_profile.profile_user).first()
            
            return UserProfileAndRoleObjects(
                id = user_profile.primary_key,
                user_profile = UserAccountBuilder.get_user_profile_data(user_profile.profile_unique_id),
                user_roles = UAABuilder.get_role_data(id=user_with_role.user_with_role_role.role_unique_id if user_with_role else None),
            )
    



