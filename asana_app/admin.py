from django.contrib import admin
from .models import ProjectModel, UserModel, TaskModel

admin.site.register(ProjectModel)
admin.site.register(UserModel)
admin.site.register(TaskModel)