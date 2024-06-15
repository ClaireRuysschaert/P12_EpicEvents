import sys
from functools import wraps
from pathlib import Path

# Adds the project path to the system's path. This allows
# to import modules from the project.
project_path = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_path)

from epicevents.views.errors import display_permission_error  # noqa


def has_permission(departments_allowed: list[int]) -> callable:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            department_id = kwargs.get("department_id")
            if department_id in departments_allowed:
                return func(*args, **kwargs)
            else:
                display_permission_error()
                return None

        return wrapper

    return decorator
