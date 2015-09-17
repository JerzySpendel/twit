from pyramid.view import view_config
from twitter.users.utils import logged_in
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from ..models import Post


@view_config(route_name='star')
@logged_in
def star(request):
    post = Post.get_by_id(request, request.matchdict['id'])
    if post not in request.user.starred:
        request.user.starred.append(post)
    else:
        raise HTTPNotFound()
    return HTTPFound(request.route_url('board'))


@view_config(route_name='unstar')
@logged_in
def unstar(request):
    post = Post.get_by_id(request, request.matchdict['id'])
    if post in request.user.starred:
        request.user.starred.remove(post)
    else:
        raise HTTPNotFound()
    return HTTPFound(location=request.route_url('favourites'))
