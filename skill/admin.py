from django.contrib import admin

from .models import *


admin.site.register(Skill)
admin.site.register(SkillCategory)
admin.site.register(SkillPerformed)