from django.db import models
import asana
from asana_app.asana_utils import AsanaApiUtils

# gid length = 31, see
# https://forum.asana.com/t/asana-is-moving-to-string-ids-updated-with-revised-timeline/29340


class ProjectManager(models.Manager):
    first_load = True

    def get_queryset(self):
        query_set = super(ProjectManager, self).get_queryset()
        if self.first_load:
            self.first_load = False
            if not query_set:
                # if it is the first run and no projects are defined in our DB
                # then let's try to fetch projects from Asana
                asana_projects = AsanaApiUtils().get_projects()
                for project in asana_projects:
                    ProjectModel(gid=project['gid'],
                                 name=project['name']).save(db_only=True)
        return query_set


class ProjectModel(models.Model):
    gid = models.CharField(primary_key=True, editable=False, max_length=31)
    name = models.CharField(max_length=200)
    objects = ProjectManager()

    def __str__(self):
        return self.name

    def save(self, db_only=False, *args, **kwargs):
        if not db_only:
            if self.gid:
                # project already exists, need to update it
                AsanaApiUtils().update_project(self.gid, self.name)
            else:
                # create new project
                self.gid = AsanaApiUtils().create_project(self.name)['gid']

        # Create project in our DB
        return super().save(*args, **kwargs)


class UserManager(models.Manager):
    first_load = True

    def get_queryset(self):
        query_set = super(UserManager, self).get_queryset()
        if self.first_load:
            self.first_load = False
            if not query_set:
                # if it is the first run and no users are defined in our DB
                # then let's try to fetch projects from Asana
                asana_users = AsanaApiUtils().get_users()
                for user in asana_users:
                    UserModel(gid=user['gid'],
                              name=user['name']).save()
        return query_set


class UserModel(models.Model):
    gid = models.CharField(primary_key=True, editable=False, max_length=31)
    name = models.CharField(max_length=200, editable=False)
    objects = UserManager()

    def __str__(self):
        return self.name


class TaskManager(models.Manager):
    first_load = True

    def get_queryset(self):
        query_set = super(TaskManager, self).get_queryset()
        if self.first_load:
            self.first_load = False
            if not query_set:
                # if it is the first run and no tasks are defined in our DB
                # then let's try to fetch projects from Asana
                asana_tasks = AsanaApiUtils().get_tasks()
                for task in asana_tasks:
                    user = None
                    if task['assignee']:
                        # make sure users are populated at first start
                        UserModel.objects.all()
                        user = UserModel(
                            gid=task['assignee']['gid'], name=task['assignee']['name'])
                    TaskModel(gid=task['gid'],
                              name=task['name'], assignee=user).save()
        return query_set


class TaskModel(models.Model):
    gid = models.CharField(primary_key=True, editable=False, max_length=31)
    name = models.CharField(max_length=200, editable=False)
    assignee = models.ForeignKey(
        to=UserModel, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(to=ProjectModel, on_delete=models.CASCADE)
    
    objects = TaskManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.gid:
            pass
        else:
            pass
            # AsanaApiUtils().create_task()

        # Create project in our DB
        return super().save(*args, **kwargs)
