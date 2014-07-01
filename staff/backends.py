# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend
from staff import get_user_model
from staff.models import Staff

class StaffBackend(ModelBackend):
    """
    OpenHouse Staff Backend
    """

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

    def _get_group_permissions(self, user_obj):
        user_groups_field = get_user_model()._meta.get_field('role')
        user_groups_query = 'role__%s' % user_groups_field.related_query_name()
        return Permission.objects.filter(**{user_groups_query: user_obj})

    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings the user `user_obj` has from the
        groups they belong.
        """
        return self._get_permissions(user_obj, obj, 'role')

    def get_user(self, user_id):
        """
        With this method,
        backend can get the correct Staff
        """
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
