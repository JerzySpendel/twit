from pyramid.view import view_config
from twitter.users.utils import logged_in


@view_config(route_name='favourites', renderer='twitter:templates/board.jinja2')
@logged_in
def favourites(request):
    return {'posts': request.user.starred}