from pyramid.view import view_config
from ..models import User
from ..utils import logged_in


@view_config(route_name='users', renderer='twitter:templates/users.jinja2')
@logged_in
def users(request):
    users = User.get_all(request)
    users.remove(request.user)
    return {'users': users}
