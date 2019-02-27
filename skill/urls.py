from django.conf.urls import url

from . import views

app_name = 'skill'
urlpatterns = [
    url(r'skillLog/$', views.skillLogView.as_view(), name='skillLog'),
    url(r'success', views.skillSuccessView.as_view(), name='success'),
    url(r'mySkills', views.mySkillsView, name='mySkills'),
    url(r'studentsSkills', views.studentsSkillsView, name='studentsSkills'),
]
