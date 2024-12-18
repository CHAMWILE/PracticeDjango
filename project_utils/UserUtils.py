import uuid
from rest_framework.permissions import IsAuthenticated

from project_account.models import UsersProfiles
from project_dtoBuilder.UAABuilder import UAABuilder
from project_uaa.models import UsersWithRoles
from project_utils.BearerTokenAuthentication import BearerTokenAuthentication


    
class UserUtils:
    def __init__(self, request):
        self.request = request
    
    
    @staticmethod
    def get_user(request=None):
        
        is_authenticated, user = BearerTokenAuthentication.authenticate(None, request)

        user_data = {}
        
        if not is_authenticated:
            return user_data
            
        profile = UsersProfiles.objects.filter(profile_user=user).first()
        
        if profile is None:
            return user_data
        
        
        user_data.update({
            'id': str(profile.profile_user_id),
            'profile_unique_id': str(profile.profile_unique_id),
            'profile_type': profile.profile_type,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email
        })
        
        return user_data
    
    
    
    def get_user_permissions(user):
        user_with_role= UsersWithRoles.objects.filter(user_with_role_user=user).first()
        if not user_with_role:
            return []
        user_roles = UAABuilder.get_role_data(id=user_with_role.user_with_role_role.unique_id)
        user_permissions =[]
        for permission in user_roles.role_permissions:
            user_permissions.append(permission.permission_code)
        return user_permissions

    
    
    @staticmethod
    def __profile__(request):
        user_data = UserUtils.get_user(request=request)
  
        if user_data:
            return user_data.get('profile_unique_id')  
        return None  
    
    
    # @staticmethod
    # def __profile__(request):
    #     return UserUtils.get_user(request)['profile_unique_id']
   
    @staticmethod
    def get_forgot_password_token():
        token =  str(uuid.uuid4())
        return token
