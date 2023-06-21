import threading

#--------------------------------------------------------- for accessing request.user in model file
class RequestMiddleware:
    def __init__(self,get_response,thread_local=threading.local()):
        self.get_response=get_response
        self.thread_local=thread_local
    def __call__(self, request):
        self.thread_local.current_request=request
        response=self.get_response(request)
        return response