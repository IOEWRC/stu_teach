from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Class
from django.urls import reverse_lazy


class ClassListView(ListView):
    model = Class
    context_object_name = 'classes'
    template_name = 'forum/class_list.html'


class ClassCreateView(CreateView):
    model = Class
    # Either use form class or fields
    fields = ['name', 'description', 'class_avatar',]
    template_name = 'forum/create_group.html'
    # template_name = 'forum/class_list.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClassDeleteView(DeleteView):
    model = Class
    success_url = reverse_lazy('forum:class_list')


class ClassUpdateView(UpdateView):
    model = Class
    template_name = 'forum/class_update.html'
    fields = fields = ['name', 'description', 'class_avatar',]

def home(request):
    return render(request, 'forum/home.html', {'user': request.user, })


class ClassQuestionAdd(CreateView):
    model = Class
    template_name = 'forum/class_question_add.html'
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
