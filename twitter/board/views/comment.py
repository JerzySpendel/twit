from pyramid.view import view_config
from twitter.users.utils import logged_in
from pyramid.httpexceptions import HTTPFound, HTTPMethodNotAllowed, HTTPForbidden, HTTPNotFound
from ..models import Post, Comment


@view_config(route_name='comment')
@logged_in
def comment(request):
    if request.method == 'POST':
        post = Post.get_by_id(request, request.matchdict['id'])
        if post is None:
            raise HTTPNotFound()
        if post.can_comment(request):
            comment = Comment.from_request(request)
            request.db.add(comment)
        else:
            raise HTTPForbidden()
    else:
        raise HTTPMethodNotAllowed()
    return HTTPFound(location=request.route_url('board'))