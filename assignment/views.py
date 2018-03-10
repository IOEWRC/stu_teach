from django.contrib.auth import get_user_model
from django.http import JsonResponse, Http404
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import Task, Assignment
from forum.models import Class


# Create your views here.
class Home(LoginRequiredMixin, View):
    template_name = 'assignment/assignment_home.html'
    login_url = settings.LOGIN_URL

    def __init__(self, **kwargs):
        pass

    def get(self, request, pk):
        # Only fetch students
        classs = get_object_or_404(Class, pk=pk)
        users = classs.students.all()
        if request.user == classs.created_by:
            tasks = Task.objects.filter(owner=request.user, classs=classs)
        elif request.user in users:
            tasks = Task.objects.filter(assignments__student=request.user, classs=classs)
        else:
            raise Http404
        assignments = Assignment.objects.filter(student=request.user)
        return render(request, self.template_name, {'users': users, 'tasks': tasks, 'classs': classs})


class TaskView(View):
    def post(self, request):
        title = request.POST.get("name")
        description = request.POST.get("description")
        studentID = request.POST.getlist("students[]")
        pk = request.POST.get("class_pk")
        # Create a new task
        user= request.user
        newTask = Task(title=title, description=description, owner=user, classs=Class.objects.get(pk=pk))
        newTask.save()
        students = get_user_model().objects.filter(id__in=studentID)
        # For assigned students create assignments
        for student in students:
            assignment = Assignment(student=student)
            assignment.save()
            newTask.assignments.add(assignment)
            newTask.save()
        return JsonResponse({"message": "Successfully Saved!"})


class AssignmentView(View):
    def post(self, request):
        assignmentID = request.POST.get("assignmentID")
        status = request.POST.get("status", None)
        description = request.POST.get("description", None)
        assignment = Assignment.objects.get(id=int(assignmentID))
        if description:
            assignment.description = description
            assignment.status = 3  # 'done' status int value
        if status:
            assignment.status = int(status)
        assignment.save()
        return JsonResponse({"message": "Status Successfully Updated!"})


class ReviewAssignmentStatus(View):
    def post(self, request):
        assignmentID = request.POST.get("assignmentID")
        status = request.POST.get("status")
        assignment = Assignment.objects.get(id=int(assignmentID))
        assignment.status = int(status)
        assignment.save()
        return JsonResponse({"message": "Assignment Reviewed Successfully!"})
