from pyramid.view import view_config
from ..models import HashTag


@view_config(route_name='hashtags', renderer='twitter:templates/hashtags.jinja2')
def hashtags(request):
    hashtag = request.matchdict['hashtag']
    return {'tag': HashTag.get_by_name(request, hashtag)}
