from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from ..models import Post
from twitter.users.utils import logged_in


@view_config(route_name='post')
@logged_in
def post(request):
    if request.method == 'POST':
        p = Post.from_request(request)
        request.db.add(p)
        return HTTPFound(location=request.route_url('board'))
