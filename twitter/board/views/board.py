from pyramid.view import view_config
from ..models import Post
from twitter.users.utils import logged_in


@view_config(route_name='board', renderer='twitter:templates/board.jinja2')
@logged_in
def board(request):
    return {'posts': Post.get_all(request)}
