from django.urls import resolve
from django.http import Http404


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        resolve_obj = resolve(request.path_info)
        request_view_namespace = resolve_obj.namespace
        if request_view_namespace == 'admin':  # TODO can be used to add pages that require admin access
            if request.user.is_superuser:
                return None
            else:
                raise Http404
        return None
