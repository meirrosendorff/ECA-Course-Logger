from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.views import View
from accounts.views import create_context_csrf, loginPage
from .models import Skill, SkillCategory
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
        #
        # username=request.POST['username'], password=request.POST['password'])
        #
        # if user is not None:
        #     login(request, user)
        #     return redirect(homePage)

        # If not true, then the user will appear on the login page and see an error message
        context = create_context_csrf(request)
        context['errorLoggingIn'] = True
        # context = addValuesToContext(context, request) # adds certain necessary info to the context
        return render(request, loginPage[1:] + ".html", context=context)