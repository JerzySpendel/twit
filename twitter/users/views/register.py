from pyramid.view import view_config
from ..models import User


@view_config(route_name='register', renderer='twitter:templates/register.jinja2')
def register(request):
    if request.method == 'POST':
        return User.register(request)
    return {}
