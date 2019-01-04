from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.views import View

loginPage = '/accounts/login'


class loginView(View):

    def get(self, request):

        # redirect if already logged in
        # if request.user.is_authenticated:

        # otherwise return the login page
        context = create_context_csrf(request)

        return render(request, loginPage[1:] + ".html", context)

    def post(self, request, *args, **kwargs):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect("/aaaaaaaaa")

        # If not true, then the user will appear on the login page and see an error message
        context = create_context_csrf(request)
        context['errorLoggingIn'] = True
        # context = addValuesToContext(context, request) # adds certain necessary info to the context
        return render_to_response(loginPage[1:] + ".html", context=context)


# logs out the user and then redirects to the login page
# if user is not logged in just redirects
class logoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect(loginPage)


# helper method to generate a context csrf_token
def create_context_csrf(request):
    context = {}
    context.update(csrf(request))
    return context

