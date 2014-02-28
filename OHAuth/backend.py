from django.contrib.auth.models import User
from staff.models import Staff

class StaffBackend(object):

    def authenticate(self, username=None, password=None):
        kwargs = {'studentid': username, 'password': password}
        try:
            user = Staff.objects.get(studentid=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
