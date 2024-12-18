import pytz
import graphene
import hashlib
import datetime
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from graphene_federation import build_schema
from django.db import transaction

from dotenv import dotenv_values

from project_account.models import ActivateAccountTokenUsers, ForgotPasswordRequestUsers, UsersProfiles
from project_dtoBuilder.UserAccountsBuilders import UserAccountBuilder
from project_dtos.Response import ResponseObject
from project_dtos.UserAccount import ForgortPasswordInputObject, SetPasswordInputObject, UserInputObject, UserProfileObject
from project_uaa.models import UserRoles, UsersWithRoles
from project_utils.UserUtils import UserUtils
from project_utils.EmailUtils import EmailNotifications
from project_utils.Validators import Validator
from project_utils.UserUtils import *


config = dotenv_values(".env")



class CreateUsersMutation(graphene.Mutation):
    class Arguments:
        input = UserInputObject(required=True)        

    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileObject) 

    @classmethod
    # @has_mutation_access(permissions=['can_create_users_mutation'])
    def mutate(self, root, info,  input):
        
        if not Validator.validate_email(input.user_email):
            return self(response=ResponseObject.get_response(id='10'))
        
        if User.objects.filter(email=input.user_email).exists():
            return self (response =  ResponseObject.get_response(id='3')) 
        
        if input.profile_phone:
            if not Validator.validate_phone_number(input.profile_phone):
                return self(response=ResponseObject.get_response(id='27'))
        
        try:
            user = User.objects.create_user(
            first_name=input.user_first_name,
            last_name=input.user_last_name,
            username=input.user_email,
            email=input.user_email,
            
        ) 
        except Exception as e:
            return self(response=ResponseObject.get_response(id="8"))
        

        user_profile = UsersProfiles.objects.create(
            profile_type=input.profile_type.value,
            profile_phone=input.profile_phone,
            profile_gender = input.profile_gender.value,
            profile_photo = input.profile_photo,
            profile_user=user
        )   
        
        
        naive_datetime = datetime.now()
        request_token = UserUtils.get_forgot_password_token()
        naive_datetime_with_timezone = timezone.make_aware(naive_datetime, timezone.utc)
        expiration_time = naive_datetime_with_timezone + timedelta(minutes=30)
        
        ActivateAccountTokenUsers.objects.create(
            token_user = user,
            token_token = request_token
        )


        url = config['FRONTEND_DOMAIN'] + f"/auth/password-set/{request_token}"

        
        body = {
            'receiver_details': user.email,
            'user': user,
            'url': url,
            'subject': "Notification Gateway Set Password EMAIL"
        }
        
        EmailNotifications.send_email_notification(body, 'emails/password_set_email.html')
        
        UsersWithRoles.objects.create(user_with_role_role = UserRoles.objects.filter(role_name = input.profile_type.value).first(),user_with_role_user=user)
        response_body = UserAccountBuilder.get_user_profile_data(id=user_profile.profile_unique_id)
        
        return self(response=ResponseObject.get_response(id="2"), data=response_body)


class UpdateUsersMutation(graphene.Mutation):
    class Arguments:
        input = UserInputObject(required=True)

    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileObject)

    @classmethod
    #@has_mutation_access(permissions=['can_update_users_mutation'])    
    def mutate(self, root, info, input):
       
        profile = UsersProfiles.objects.filter(profile_is_active=True, profile_unique_id=input.profile_unique_id).first()
        
        if profile is None:
            return self(response=ResponseObject.get_response(id="22"), data=None)

        profile.profile_phone = input.profile_phone
        profile.profile_photo = input.profile_photo
        profile.profile_type=input.profile_type.value
        profile.profile_gender = input.profile_gender.value
        profile.save()

        profile.profile_user.first_name = input.user_first_name
        profile.profile_user.last_name = input.user_last_name
        profile.profile_user.email = input.user_email
        profile.profile_user.save()

        
        UsersWithRoles.objects.filter(user_with_role_user=profile.profile_user).update(
            user_with_role_role = UserRoles.objects.filter(role_name = input.profile_type.value).first(),
        )
        
        response_body = UserAccountBuilder.get_user_profile_data(id=profile.profile_unique_id)
        return self(response=ResponseObject.get_response(id="1"), data=response_body)
        


class DeleteUsersMutation(graphene.Mutation):
    class Arguments:
        profile_unique_id = graphene.String(required=True)

    response = graphene.Field(ResponseObject)

    @classmethod
    #@has_mutation_access(permissions=['can_delete_users_mutation'])
    def mutate(self, root, info,  profile_unique_id):

        admin_profile = UsersProfiles.objects.filter(profile_unique_id=profile_unique_id).first()

        admin_profile.profile_type = ""
        admin_profile.profile_is_active = False
        admin_profile.save()
        admin_profile.profile_user.is_active = False
        admin_profile.profile_user.save()

        return self(response=ResponseObject.get_response(id="1"))



class UpdateMyProfileMutation(graphene.Mutation):
    class Arguments:
        input = UserInputObject()

    response = graphene.Field(ResponseObject)
    data = graphene.Field(UserProfileObject)

    @classmethod
    # @has_mutation_access(permissions=['can_update_my_profile_mutation'])    
    def mutate(self, root, info, input):
        profile_id = UserUtils.__profile__(info.context.headers)
 
        profile = UsersProfiles.objects.filter(profile_unique_id=profile_id, profile_is_active=True).first()
        if profile is None:
            return self(response=ResponseObject.get_response(id="22"), data=None)

        UsersWithRoles.objects.filter(user_with_role_user=profile.profile_user).update(
            user_with_role_role = UserRoles.objects.filter(role_name = input.profile_type.value).first(),
        )
        
        profile.profile_phone = input.profile_phone
        profile.profile_photo = input.profile_photo
        profile.profile_type=input.profile_type.value
        profile.profile_gender = input.profile_gender.value
        profile.save()

        profile.profile_user.first_name = input.user_first_name
        profile.profile_user.last_name = input.user_last_name
        profile.profile_user.email = input.user_email
        profile.profile_user.save()
        
        
        response_body = UserAccountBuilder.get_user_profile_data(id=profile.profile_unique_id)
        return self(response=ResponseObject.get_response(id="1"), data=response_body)

   


class ForgotPasswordMutation(graphene.Mutation):
    class Arguments:
        user_email = graphene.String(required=True)
    
    response = graphene.Field(ResponseObject)
    
    @classmethod
    # @has_mutation_access(permissions=['can_forgot_password_mutation'])
    def mutate(self, root, info, user_email):
        user = User.objects.filter(username=user_email).first()
        if user is None:
            return self(response=ResponseObject.get_response(id="10"))
        
        request_token = UserUtils.get_forgot_password_token()
        
        naive_datetime = datetime.now()
        naive_datetime_with_timezone = timezone.make_aware(naive_datetime, timezone.utc)
        expiration_time = naive_datetime_with_timezone + timedelta(minutes=30)
        
        ForgotPasswordRequestUsers.objects.create(
            request_user=user,
            request_token=request_token,
            request_expiration_time=expiration_time  
        )
        
        url = config['FRONTEND_DOMAIN'] + f"/auth/password-reset/{request_token}"

        body = {
            'receiver_details': user.email,
            'user': user,
            'url': url,
            'subject': "Django BoilerPlate System Re-Set Password"
        }
        
        EmailNotifications.send_email_notification(body, 'emails/password_reset_email.html')
        return self(response=ResponseObject.get_response(id="11"))



class ResetPasswordMutation(graphene.Mutation):
    class Arguments:
        input = SetPasswordInputObject()
    
    response = graphene.Field(ResponseObject)
    
    @classmethod
    # @has_mutation_access(permissions=['can_reset_password_mutation'])
    def mutate(self, root, info, input):
        
        requested_token = ForgotPasswordRequestUsers.objects.filter(request_token = input.request_token, request_is_used=False).first()
        
        if requested_token is None:
            return self(response = ResponseObject.get_response(id="14"))
        
        if input.user_password != input.confirm_password:
                return self(response= ResponseObject.get_response(id="17"))
        
        if not Validator.is_strong_password(input.user_password):
            return self(response=ResponseObject.get_response(id='28'))
        
        current_datetime = datetime.now(pytz.UTC)
        request_token_expired = requested_token.request_expiration_time < current_datetime
        

        if request_token_expired or requested_token is None:
            return self(response= ResponseObject.get_response(id="18"))
        
        user =requested_token.request_user
        user.set_password(input.user_password)
        user.save()
        requested_token.request_is_used = True
        requested_token.save()

        return self(response=ResponseObject.get_response(id="1"))
    
        
        
class ChangePasswordMutation(graphene.Mutation):
    class Arguments:
        input = ForgortPasswordInputObject()
    response = graphene.Field(ResponseObject)

    @classmethod
    # @has_mutation_access(permissions=['can_change_password_mutation'])
    def mutate(cls, root, info, input):
        
        user_data = UserUtils.__profile__(info.context.headers)
        if user_data is None:
            return cls(response=ResponseObject.get_response(id="6"))
        user_profile = UsersProfiles.objects.filter(
            profile_unique_id = user_data
        ).first()                     
        
        user = User.objects.get(pk=user_profile.profile_user.pk)
        
        if not Validator.is_strong_password(input.new_password):
            return cls(response=ResponseObject.get_response(id='28'))
        
        if not user.check_password(input.old_password):
            return cls(response=ResponseObject.get_response(id="12"))
        
        new_password_hashed = Validator.hash_password(input.new_password)
      
        if input.old_password == input.new_password:
            return cls(response=ResponseObject.get_response(id="12"))
        
        user.set_password(input.new_password)
        user.save()
        user_profile.profile_default_password = False
        user_profile.save()
        
        return cls(response=ResponseObject.get_response(id='1'))

        


class SetPasswordMutation(graphene.Mutation):
    class Arguments:
        input = SetPasswordInputObject()
    
    response = graphene.Field(ResponseObject)
    
    @classmethod
    # @has_mutation_access(permissions=['can_set_password_mutation'])
    def mutate(self, root, info, input):
        try: 
            requested_token = ActivateAccountTokenUsers.objects.filter( token_token= input.request_token, token_is_used = False).first()
            print(">>>>>>>>>>>>>>>>>", requested_token)
            if requested_token is None:
                return self(response= ResponseObject.get_response(id="18"))
            
            if input.user_password != input.confirm_password:
                return self(response= ResponseObject.get_response(id="17"))
            
            if not Validator.is_strong_password(input.user_password):
                return self(response=ResponseObject.get_response(id='28'))
            
            user =requested_token.token_user
            user.set_password(input.user_password)
            user.save()
            
            requested_token.token_is_used = True
            requested_token.save()
           
            profile = UsersProfiles.objects.filter(profile_user=user, profile_is_active=True).first()
            profile.profile_has_been_verified=True
            profile.save()
            
            return self(response=ResponseObject.get_response(id="1"))
        except:
            return self(response=ResponseObject.get_response(id="5"))


class Mutation(graphene.ObjectType):
    create_users_mutation = CreateUsersMutation.Field()
    update_users_mutation = UpdateUsersMutation.Field()
    delete_users_mutation = DeleteUsersMutation.Field()
    
    update_my_profile_mutation = UpdateMyProfileMutation.Field()
    forgot_password_mutation = ForgotPasswordMutation.Field()
    reset_password_mutation = ResetPasswordMutation.Field()
    change_password_mutation = ChangePasswordMutation.Field()
    set_password_mutation = SetPasswordMutation.Field()

schema = build_schema(Mutation, types=[])

   