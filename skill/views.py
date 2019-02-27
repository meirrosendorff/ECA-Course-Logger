from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.views import View
from accounts.views import create_context_csrf, loginPage, addImportantContext
from .models import Skill, SkillCategory, SkillPerformed
from shifts.models import Service
import datetime
from django.contrib.auth.models import User

skillLogPage = "/skill/skillLog"


class skillLogView(View):

    def get(self, request):

        context = create_context_csrf(request)

        # redirect if already logged in
        if not request.user.is_authenticated:
            return redirect(loginPage)

        context = addImportantContext(request, context)

        services = Service.objects.all()
        skills = Skill.objects.all()
        categories = SkillCategory.objects.all()


        context['skills'] = skills
        context['categories'] = categories
        context['services'] = services
        context['date'] = datetime.datetime.today().strftime('%Y-%m-%d')
        context['time'] = datetime.datetime.today().strftime('%H:%M')

        return render(request, skillLogPage[1:] + ".html", context)

    def post(self, request, *args, **kwargs):

        currSkill = request.POST['skills']
        currService = request.POST['service']
        currSupervisor = request.POST['supervisor']
        date = request.POST['date']
        time = request.POST['time']
        comment = request.POST['comment']

        newSkill = SkillPerformed()


        newSkill.user = request.user
        newSkill.skill = Skill.objects.get(skillID=currSkill)
        newSkill.service = Service.objects.get(serviceID=currService)
        newSkill.supervisor = currSupervisor
        newSkill.date = date
        newSkill.time = time
        newSkill.comment = comment

        newSkill.save()

        return redirect("/skill/success")

class skillSuccessView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(loginPage)
        else:
            context = create_context_csrf(request)
            context = addImportantContext(request, context)

            return render(request, "skill/success.html", context)

def mySkillsView(request, user=None):

    context = create_context_csrf(request)

    # redirect if not already logged in
    if not request.user.is_authenticated:
        return redirect(loginPage)

    context = addImportantContext(request, context)


    if user is None:
        user = request.user

    context['username'] = user.first_name + " " + user.last_name

    catagories = SkillCategory.objects.all()

    currSkills = SkillPerformed.objects.filter(user=user)

    skillSummary = []

    for type in catagories:
        typeSummary = []

        typeSkills = currSkills.filter(skill__skillCategory__name=type.name)

        skillNames = Skill.objects.filter(skillCategory__name=type.name)

        for name in skillNames:

            curr = typeSkills.filter(skill__name=name.name)

            typeSummary.append((name, name.skillID, len(curr), curr))

        skillSummary.append(typeSummary)

    context['summary'] = skillSummary

    return render(request, "skill/skillSummary.html", context)

def studentsSkillsView(request):
    # redirect if not already logged in
    if not request.user.is_authenticated:
        return redirect(loginPage)

    context = create_context_csrf(request)
    context = addImportantContext(request, context)

    if not request.user.is_staff:
        return render(request, "notStaff.html", context)

    if request.method == "GET":

        students = User.objects.filter(is_staff=False)

        studentList = [(student.username, student.first_name + " " + student.last_name) for student in students]

        context['studentList'] = studentList

        return render(request, "skill/studentsSkills.html", context)

    if request.method == "POST":

        try:

            username = request.POST['username']

            user = User.objects.get(username=username)

            context['username'] = username

            return mySkillsView(request, user)

        except:

            return render(request, "error.html", context)
