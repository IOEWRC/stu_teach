from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, TemplateView
from .models import Class, Question, Answer, Reply
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .forms import (
    ClassCreateForm, QuestionCreateForm, AnswerCreateForm, ReplyCreateForm, JoinForm, DeleteForm
)
from django.contrib.auth.models import User
from django.http import JsonResponse


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
    joined_classes = Class.objects.filter(students=request.user).order_by('-created_at')
    started_classes = Class.objects.filter(created_by=request.user).order_by('-created_at')

    j_page = request.GET.get('j_page', 1)
    j_paginator = Paginator(joined_classes, 4)
    s_page = request.GET.get('s_page', 1)
    s_paginator = Paginator(started_classes, 4)
    try:
        joined_classes = j_paginator.page(j_page)
        started_classes = s_paginator.page(s_page)
    except PageNotAnInteger:
        joined_classes = j_paginator.page(1)
        started_classes = s_paginator.page(1)
    except EmptyPage:
        joined_classes = j_paginator.page(j_paginator.num_pages)
        started_classes = s_paginator.page(s_paginator.num_pages)
    joined_classes.page_url_label = 'j_page'
    started_classes.page_url_label = 's_page'

    if request.method == 'POST':
        j_form = JoinForm(request.POST)
        c_form = ClassCreateForm(request.POST, request.FILES)
        del_form = DeleteForm(request.POST)

        if j_form and j_form.is_valid():
            code = j_form.cleaned_data['code']
            try:
                class_object = Class.objects.get(code=code)
                if class_object:
                    class_object.students.add(request.user)
                    class_pk = class_object.pk
                    messages.success(request, 'Welcome to Class')
                    return redirect('forum:class_detail', pk=class_pk)
            except Class.DoesNotExist:
                pass
            c_form = ClassCreateForm()
            del_form = DeleteForm()
            messages.warning(request, 'No class Found. Enter the correct invitation code.')
            return render(request, 'forum/home.html', {
                'j_form': j_form,
                's_classes': started_classes,
                'j_classes': joined_classes,
                'c_form': c_form,
                'del_form': del_form,
            })
        elif c_form and c_form.is_valid():
            try:
                classs = c_form.save(commit=False)
                classs.created_by = request.user
                classs.save()
                messages.success(request, 'Class created successfully.')
                return redirect('forum:class_detail', pk=classs.pk)
            except Exception as e:
                messages.warning(request, "Failed To Create. Error: {}".format(e))
            j_form = JoinForm()
            del_form = DeleteForm()
            messages.warning(request, "Failed To Create Check Errors")
            return render(request, 'forum/home.html', {
                'j_form': j_form,
                's_classes': started_classes,
                'j_classes': joined_classes,
                'c_form': c_form,
                'del_form': del_form,
            })
        elif del_form and del_form.is_valid():
            try:
                classs = Class.objects.get(pk=request.POST.get('delete_class_pk'))
                classs.delete()
                messages.success(request, 'Class deleted successfully.')
                return redirect('forum:home')
            except Exception as e:
                pass
            messages.warning(request, 'Failed to delete class.')
            j_form = JoinForm()
            c_form = ClassCreateForm()
            return render(request, 'forum/home.html', {
                'j_form': j_form,
                's_classes': started_classes,
                'j_classes': joined_classes,
                'c_form': c_form,
                'del_form': del_form,
            })
    else:
        j_form = JoinForm()
        c_form = ClassCreateForm()
        del_form = DeleteForm()
        return render(request, 'forum/home.html', {
            'j_form': j_form,
            's_classes': started_classes,
            'j_classes': joined_classes,
            'c_form': c_form,
            'del_form': del_form,
        })
        del_form = DeleteForm()
        return render(request, 'forum/home.html', {
            'j_form': j_form,
            's_classes': started_classes,
            'j_classes': joined_classes,
            'c_form': c_form,
            'del_form': del_form,
        })


def vote_question(request, operation, pk):
    upvoted_user = request.user
    question = get_object_or_404(Question, pk=pk)
    upvoted_users = question.upvoted_by.all()
    downvoted_users = question.downvoted_by.all()

    try:
        if operation == 'upvote':
            if upvoted_user in downvoted_users:
                question.downvoted_by.remove(upvoted_user)
                question.votes += 1
                question.save()
            elif upvoted_user not in upvoted_users:
                question.upvoted_by.add(upvoted_user)
                question.votes += 1
                question.save()
        elif operation == 'downvote':
            if upvoted_user in upvoted_users:
                question.upvoted_by.remove(upvoted_user)
                question.votes -= 1
                question.save()
            elif upvoted_user not in downvoted_users:
                question.downvoted_by.add(upvoted_user)
                question.votes -= 1
                question.save()
    except (KeyError, Answer.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True, 'votes': question.votes})

    # return redirect('forum:class_detail', pk=question.class_room.pk)

