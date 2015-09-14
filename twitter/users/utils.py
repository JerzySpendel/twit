from functools import wraps
from .models import User


def logged_in(view):

    @wraps(view)
    def wrapper(request, *vargs, **kwargs):
        user = User.get_by_username(request, request.authenticated_userid)
        request.user = user
        return view(request, *vargs, **kwargs)

    return wrapper