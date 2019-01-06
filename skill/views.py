from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.views import View
from accounts.views import create_context_csrf, loginPage
from .models import Skill, SkillCategory, SkillPerformed
from shifts.models import Service
import datetime

skillLogPage = "/skill/skillLog"


class skillLogView(View):

    def get(self, request):

        context = create_context_csrf(request)

        # redirect if already logged in
        if not request.user.is_authenticated:
            return redirect(loginPage)
        else:
            context['loggedIn'] = True

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
            context['loggedIn'] = True

            return render(request, "skill/success.html", context)