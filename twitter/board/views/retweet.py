from pyramid.view import view_config
from ..models import Post
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPForbidden
from twitter.users.utils import logged_in


@view_config(route_name='retweet')
@logged_in
def retweet(request):
    post_id = request.matchdict['id']
    post = Post.get_by_id(request, post_id)
    if post is None:
        raise HTTPNotFound()
    if post.has_access(request):
        retweeted_post = post.retweet(request)
        request.db.add(retweeted_post)
    else:
        raise HTTPForbidden()
    return HTTPFound(location=request.route_url('board'))
