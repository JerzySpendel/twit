class RequestToJinja:
    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        response = self.handler(request)
        if isinstance(response, dict):
            response['request'] = request
        return response
