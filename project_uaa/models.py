import uuid
from xml.dom import ValidationErr
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class UserRoles(models.Model):
    primary_key = models.AutoField(primary_key=True)
    role_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    role_name = models.CharField(default='', max_length=9000)
    role_description = models.CharField(default='', max_length=9000)
    role_is_system_default = models.BooleanField(default=False) 
    role_is_active = models.BooleanField(default=True)
    role_created_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        ordering = ['-primary_key']
        verbose_name_plural = "01.USER ROLES"

    def __str__(self):
        return "{}".format(self.role_name)

    def get_role_permissions(self):
        return self.user_role_with_permission_role.all()


class UserPermissionsGroup(models.Model):
    primary_key = models.AutoField(primary_key=True)
    permission_group_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    permission_group_name = models.CharField(default='', max_length=9000)
    permission_group_is_global = models.BooleanField(default=False)
    permission_group_description = models.CharField(default='', max_length=600, null=True)
    permission_group_created_by = models.ForeignKey(User, related_name='permission_group_creator',on_delete=models.CASCADE)
    permission_group_created_date = models.DateField(auto_now_add=True)


    class Meta:
        db_table = 'user_permissions_group'
        ordering = ['-primary_key']
        verbose_name_plural = "02.PERMISSIONS GROUP"
    
    def __str__(self):
        return "{} - {}".format(self.permission_group_name, self.permission_group_description)
    
    def get_group_permisions(self):
        return self.permission_group.all()


class UserPermissions(models.Model):
    primary_key = models.AutoField(primary_key=True)
    permission_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    permission_name = models.CharField(default='', max_length=9000)
    permission_code = models.CharField(default='', max_length=9000)
    permission_group = models.ForeignKey(UserPermissionsGroup, related_name='permission_group',on_delete=models.CASCADE, null=True)
    permission_created_by = models.ForeignKey(User, related_name='user_permission_creator', on_delete=models.CASCADE)
    permission_created_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_permissions'
        ordering = ['-primary_key']
        verbose_name_plural = "03.USER PERMISSIONS"

    def __str__(self):
        return "{} - {}".format(self.permission_name, self.permission_group)


class UserRolesWithPermissions(models.Model):
    primary_key = models.AutoField(primary_key=True)
    role_with_permission_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    role_with_permission_role = models.ForeignKey(UserRoles, related_name='user_role_with_permission_role',on_delete=models.CASCADE)
    role_with_permission_permission = models.ForeignKey(UserPermissions,related_name='user_role_with_permission_permission',on_delete=models.CASCADE)
    role_with_permission_is_active = models.BooleanField(default=True)
    permission_read_only = models.BooleanField(default=True)
    role_with_permission_created_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_role_with_permissions'
        ordering = ['-primary_key']
        verbose_name_plural = "04.ROLES WITH PERMISSIONS"

    def clean(self):
        super().clean()

        # Check if the UserRolesWithPermissions instance collides with another entry
        colliding_entries = UserRolesWithPermissions.objects.filter(role_with_permission_role=self.role_with_permission_role,role_with_permission_permission=self.role_with_permission_permission).all()

        if colliding_entries.exists():
            raise ValidationError("Permissions collides with another Role entry.")


class UsersWithRoles(models.Model):
    primary_key = models.AutoField(primary_key=True)
    user_with_role_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    user_with_role_role = models.ForeignKey(UserRoles, related_name='user_role_name', on_delete=models.CASCADE)
    user_with_role_user = models.ForeignKey(User, related_name='role_user', on_delete=models.CASCADE)
    user_with_role_created_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_with_roles'
        ordering = ['-primary_key']
        verbose_name_plural = "05.USERS WITH ROLES"

