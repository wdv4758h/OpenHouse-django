from company.models import Company

def get_user_model():
    """
    Returns the Company model
    """
    try:
        return Company
    except ValueError:
        raise ImproperlyConfigured('Company get_user_model value error')
    except LookupError:
        raise ImproperlyConfigured('Company get_user_model lookup error')
