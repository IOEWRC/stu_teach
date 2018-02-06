from django.urls import resolve, reverse_lazy
from django.conf import settings
from django.shortcuts import redirect


# EXEMPT_VIEWS = list(map(lambda x: x.func, list(
#     map(resolve, list(map(reverse_lazy, getattr(
#         settings, 'LOGIN_EXEMPT_VIEWS', []) +
#         [settings.LOGIN_URL, ]
#     ))))))

EXEMPT_VIEWS = getattr(settings, 'LOGIN_EXEMPT_VIEWS', []) + [settings.LOGIN_URL, ]


class LoginRequiredMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        request_view = resolve(request.path_info).url_name

        if request.user.is_authenticated and (request_view in EXEMPT_VIEWS):
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated or (request_view in EXEMPT_VIEWS):
            return None
        else:
            return redirect(settings.LOGIN_URL)
