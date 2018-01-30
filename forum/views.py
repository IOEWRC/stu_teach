from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView
from .models import Class
from django.urls import reverse_lazy


class ClassListView(ListView):
    model = Class
    context_object_name = 'classes'
    template_name = 'forum/class_list.html'


class ClassCreateView(CreateView):
    model = Class
    # Either use form class or fields
    fields = ['name', 'description', ]
    template_name = 'forum/class_create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClassDeleteView(DeleteView):
    model = Class
    success_url = reverse_lazy('forum:class_list')


def home(request):
    return render(request, 'forum/home.html', {'user': request.user, })

