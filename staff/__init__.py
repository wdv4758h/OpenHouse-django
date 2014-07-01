from staff.models import Staff

def get_user_model():
    """
    Returns the Staff model
    """
    try:
        return Staff
    except ValueError:
        raise ImproperlyConfigured('Staff get_user_model value error')
    except LookupError:
        raise ImproperlyConfigured('Staff get_user_model lookup error')
