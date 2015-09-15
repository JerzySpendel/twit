from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget


@view_config(route_name='logout')
def logout(request):
    r = HTTPFound(location='/')
    r.headerlist.extend(forget(request))
    return r