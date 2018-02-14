from django.urls import resolve
from forum.models import Class
from django.http import Http404
from django.shortcuts import get_object_or_404


class ClassAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        resolve_obj = resolve(request.path_info)
        request_view = resolve_obj.namespace + ':' + resolve_obj.url_name if resolve_obj.namespace else resolve_obj.url_name

        if request_view == 'forum:class_detail':
            try:
                class_pk = view_kwargs['pk']
                requested_class = get_object_or_404(Class, pk=class_pk)
                if request.user in requested_class.students.all() or request.user == requested_class.created_by:
                    return None
                else:
                    raise Http404
            except KeyError:
                pass
        return None
