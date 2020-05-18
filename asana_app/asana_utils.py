import os
import asana


class AsanaApiUtils:
    def __init__(self):
        self.client = asana.Client.access_token(os.environ.get('ASANA_PERSONAL_TOKEN'))
        self.workspace_gid = self.get_default_workspace()['gid']

    def get_default_workspace(self):
        workspaces = self.client.workspaces.get_workspaces()
        return list(workspaces)[0]

    def get_projects(self):
        projects = self.client.projects.get_projects(
            workspace=self.workspace_gid)
        return list(projects)

    def create_project(self, name):
        print(f'Creating project {name}')
        response = self.client.projects.create_project(
            {'name': name, 'workspace': self.workspace_gid})
        return response

    def update_project(self, gid, name):
        print(f'Updating project {gid} to name {name}')
        self.client.projects.update_project(
            gid, {'name': name, 'workspace': self.workspace_gid})

    def get_users(self):
        return self.client.users.get_users(workspace=self.workspace_gid)

    def create_task(self, project, name, assignee=None):
        return self.client.tasks.create({'projects': project, 'name': name})

    def get_tasks(self):
        tasks = []
        for project in self.get_projects():
            tasks_in_project = self.client.tasks.get_tasks_for_project(
                project['gid'], opt_fields=['name', 'assignee.gid', 'assignee.name'])
            tasks.extend(list(tasks_in_project))
        return tasks
