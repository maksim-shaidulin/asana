from django.apps import AppConfig
from .models import ProjectModel
from asana_utils import AsanaApiUtils


class AsanaAppConfig(AppConfig):
    name = 'asana_app'
