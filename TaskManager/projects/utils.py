from projects.models import Project, ProjectMember
from user.middleware import get_current_user


def get_user_role(project:Project) -> str:
    user_role = ProjectMember.objects.get(project=project, user=get_current_user()).user_role

    return user_role
