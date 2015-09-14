from pyramid.security import remember
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from ..models import User


@view_config(route_name='login', renderer='twitter:templates/login.jinja2')
def login(request):
    r = HTTPFound(location=request.route_url('board'))
    if request.method == 'POST':
        u = User.login(request)
        if u:
            r.headerlist.extend(remember(request, u))
            return r
        return {'message': "There's no such a user"}
    return {}
