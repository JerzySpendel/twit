from pyramid.httpexceptions import HTTPFound, HTTPMethodNotAllowed
from pyramid.view import view_config
from ..models import Post
from twitter.users.utils import logged_in


@view_config(route_name='post')
@logged_in
def post(request):
    if request.method == 'POST':
        p = Post.from_request(request)
        p.register_hashtags(request)
        return HTTPFound(location=request.route_url('board'))
    raise HTTPMethodNotAllowed()
