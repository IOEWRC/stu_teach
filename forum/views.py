from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from .models import Class, Question, Answer, Reply
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .forms import (
    ClassCreateForm, QuestionCreateForm, AnswerCreateForm, ReplyCreateForm, JoinForm
)
from django.contrib.auth.models import User
from django.db.models import Q


# class ClassListView(ListView):
#     model = Class
#     context_object_name = 'classes'
#     template_name = 'forum/class_list.html'


class ClassListView(TemplateView):
    template_name = 'forum/class_list.html'

    def get(self, request, *args, **kwargs):
        form = ClassCreateForm()
        classes = Class.objects.all()
        args = {'form': form, 'classes': classes}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        form = ClassCreateForm(request.POST)
        try:
            if form.is_valid():
                classs = form.save(commit=False)
                classs.created_by = request.user
                classs.save()
                messages.success(request, 'Class created successfully.')
                return redirect('forum:class_detail', pk=classs.pk)

        except Exception as e:
            messages.warning(request, "Failed To Create. Error: {}".format(e))
        messages.warning(request, "Failed To Create Check Errors")
        classes = Class.objects.all()
        args = {'form': form, 'classes': classes}
        return render(request, self.template_name, args)

# class ClassCreateView(CreateView):
#     model = Class
#     # Either use form class or fields
#     fields = ['name', 'description', 'class_avatar', ]
#     template_name = 'forum/class_create.html'
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)


class ClassDetailView(DetailView):
    model = Class
    context_object_name = 'class'
    template_name = 'forum/class_detail.html'


class ClassDetailView(TemplateView):
    template_name = 'forum/class_detail.html'

    def get(self, request, *args, **kwargs):
        form = QuestionCreateForm()
        single_class = get_object_or_404(Class, pk=self.kwargs['pk'])
        args = {'form': form, 'class': single_class}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        form = QuestionCreateForm(request.POST)
        class_pk = self.kwargs['pk']
        if form.is_valid():
            questions = form.save(commit=False)
            questions.created_by = User.objects.get(pk=request.user.pk)
            questions.class_room = Class.objects.get(pk=class_pk)
            questions.save()

            return redirect('forum:class_detail', pk=class_pk)

        args = {'form': form}
        return render(request, self.template_name, args)


class ClassDeleteView(DeleteView):
    model = Class
    success_url = reverse_lazy('forum:class_list')

#
# class QuestionCreateView(CreateView):
#     model = Question
#     fields = ['title', 'instruction', 'files', ]
#     template_name = 'forum/question_create.html'
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         form.instance.class_room = Class.objects.get(pk=self.kwargs['pk'])
#         return super().form_valid(form)

#
# class QuestionDetailView(DetailView):
#     model = Question
#     template_name = 'forum/question_detail.html'


class QuestionDetailView(TemplateView):
    template_name = 'forum/question_detail.html'

    def get(self, request, *args, **kwargs):
        form = AnswerCreateForm()
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        args = {'form': form, 'question': question}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        form = AnswerCreateForm(request.POST)
        class_pk = self.kwargs['pk']
        if form.is_valid():
            question_pk = self.kwargs['pk']
            answer = form.save(commit=False)
            answer.created_by = User.objects.get(pk=request.user.pk)
            answer.question = Question.objects.get(pk=question_pk)
            answer.save()

            return redirect('forum:question_detail', pk=class_pk)

        args = {'form': form}
        return render(request, self.template_name, args)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['title', 'instruction', ]
    template_name = 'forum/question_update.html'


class QuestionDeleteView(DeleteView):
    model = Question

    def get_success_url(self):
        return reverse_lazy('forum:class_detail', kwargs={'pk': self.get_object().class_room.pk})


class ClassUpdateView(UpdateView):
    model = Class
    template_name = 'forum/class_update.html'
    fields = fields = ['name', 'description', 'class_avatar',]

#
# def home(request):
#     return render(request, 'forum/home.html', {'user': request.user, })


# class AnswerCreateView(CreateView):
#     model = Answer
#     fields = ['body', 'files']
#     template_name = 'forum/reply_create.html'
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         form.instance.question = Question.objects.get(pk=self.kwargs['pk'])
#         return super().form_valid(form)

#
# class AnswerDetailView(DetailView):
#     model = Answer
#     template_name = 'forum/answer_detail.html'


class AnswerDetailView(DetailView):
    template_name = 'forum/answer_detail.html'

    def get(self, request, *args, **kwargs):
        form = ReplyCreateForm()
        answer = get_object_or_404(Answer, pk=self.kwargs['pk'])
        args = {'form': form, 'answer': answer}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        form = ReplyCreateForm(request.POST)
        answer_pk = self.kwargs['pk']
        if form.is_valid():
            question_pk = self.kwargs['pk']
            reply = form.save(commit=False)
            reply.created_by = request.user
            reply.answer = Answer.objects.get(pk=answer_pk)
            reply.save()

            return redirect('forum:answer_detail', pk=answer_pk)

        args = {'form': form}
        return render(request, self.template_name, args)


class AnswerUpdateView(UpdateView):
    model = Answer
    fields = ['body', 'files', ]
    template_name = 'forum/answer_update.html'


class AnswerDeleteView(DeleteView):
    model = Answer

    def get_success_url(self):
        return reverse_lazy('forum:question_detail', kwargs={'pk': self.get_object().question.pk})


# class ReplyCreateView(CreateView):
#     model = Reply
#     fields = ['body',]
#     template_name = 'forum/reply_create.html'
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         form.instance.answer = Answer.objects.get(pk=self.kwargs['pk'])
#         return super().form_valid(form)


class ReplyUpdateView(UpdateView):
    model = Reply
    fields = ['body', ]
    template_name = 'forum/reply_update.html'


class ReplyDeleteView(DeleteView):
    model = Reply

    def get_success_url(self):
        return reverse_lazy('forum:answer_detail', kwargs={'pk': self.get_object().answer.pk})


def home(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        c_form = ClassCreateForm(request.POST, request.FILES)

        if form and form.is_valid():
            code = form.cleaned_data['code']
            try:
                class_object = Class.objects.get(code=code)
                if class_object:
                    class_object.students.add(request.user)
                    class_pk = class_object.pk
                    messages.success(request, 'Welcome to Class')
                    return redirect('forum:class_detail', pk=class_pk)
            except Class.DoesNotExist:
                form = JoinForm()
            messages.warning(request, 'No class Found. Enter the correct invitation code.')
            return render(request, 'forum/home.html', {'form': form, 'c_form': c_form})

        else:
            try:
                if c_form.is_valid():
                    if c_form.is_valid():
                        classs = c_form.save(commit=False)
                        classs.created_by = request.user
                        classs.save()
                        messages.success(request, 'Class created successfully.')
                        return redirect('forum:class_detail', pk=classs.pk)
            except Exception as e:
                messages.warning(request, "Failed To Create. Error: {}".format(e))
            messages.warning(request, "Failed To Create Check Errors")
            return render(request, 'forum/home.html', {'form': form, 'c_form': c_form})
    else:
        selected_user = request.user
        joined_classes = Class.objects.filter(Q(students=selected_user))
        started_classes = Class.objects.filter(created_by=selected_user)
        form = JoinForm()
        c_form = ClassCreateForm()
        return render(request, 'forum/home.html', {'form': form,  's_classes': started_classes,
                                                   'j_classes': joined_classes, 'c_form': c_form})










