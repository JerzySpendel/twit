from pyramid.httpexceptions import HTTPFound


class RequestToJinja:
    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        response = self.handler(request)
        if isinstance(response, dict):
            response['request'] = request
        return response


class RedirectIfLogged:
    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        if request.path == '/' or request.path == '/login':
            if request.authenticated_userid is not None:
                return HTTPFound(location=request.route_url('board'))
        return self.handler(request)
