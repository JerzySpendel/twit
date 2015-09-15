from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..utils import logged_in
from ..models import User


@view_config(route_name='follow')
@logged_in
def follow(request):
    username = request.matchdict['username']
    u = User.get_by_username(request, username)
    if u is None:
        raise HTTPNotFound("No such a user")
    u.followers.append(request.user)
    request.db.add(u)
    return HTTPFound(location=request.route_url('users'))
