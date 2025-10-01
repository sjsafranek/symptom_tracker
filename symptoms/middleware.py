
# class AuthRequiredMiddleware(object):
#     def process_request(self, request):
#         if not request.user.is_authenticated():
#             return HttpResponseRedirect(reverse('landing_page')) # or http response
#         return None


# class AuthRequiredMiddleware(object):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.

#         response = self.get_response(request)
#         if not request.user.is_authenticated: # in Django > 3 this is a boolean
#             return HttpResponseRedirect('login')
        
#         # Code to be executed for each request/response after
#         # the view is called.

#         return response