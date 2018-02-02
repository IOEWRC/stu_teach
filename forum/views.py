from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from .models import Class, Question
from django.urls import reverse_lazy


class ClassListView(ListView):
    model = Class
    context_object_name = 'classes'
    template_name = 'forum/class_list.html'


class ClassCreateView(CreateView):
    model = Class
    # Either use form class or fields
    fields = ['name', 'description', 'class_avatar', ]
    template_name = 'forum/class_create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClassDetailView(DetailView):
    model = Class
    context_object_name = 'class'
    template_name = 'forum/class_detail.html'


class ClassDeleteView(DeleteView):
    model = Class
    success_url = reverse_lazy('forum:class_list')


class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'instruction', ]
    template_name = 'forum/question_create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.class_room = Class.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class QuestionDetailView(DetailView):
    model = Question
    pk_url_kwarg = 'pk'
    template_name = 'forum/question_detail.html'


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['title', 'instruction', ]
    template_name = 'forum/question_update.html'


class QuestionDeleteView(DeleteView):
    model = Question

    def get_success_url(self):
        return reverse_lazy('forum:class_detail', kwargs={'pk': self.get_object().class_room.pk})


def home(request):
    return render(request, 'forum/home.html', {'user': request.user, })
