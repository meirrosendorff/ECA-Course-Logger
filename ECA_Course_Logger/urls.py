"""ECA_Course_Logger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from accounts.views import loginView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'accounts/', include('accounts.urls'), name='accounts'),
    url(r'skill/', include('skill.urls'), name='skill'),
    url(r'shifts/', include('shifts.urls'), name='shift'),
    url(r'^$', loginView.as_view(), name='login')

]
