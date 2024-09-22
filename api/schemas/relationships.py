"""
Pydantic validation models for entity relationship 
requests and responses.

(Module necessary to avoid circular dependencies between entity models)

"""

from typing import List, Optional
from api.schemas.customer import CustomerOut
from api.schemas.project import ProjectOut
from api.schemas.user import UserOut


class ProjectWithUsersOut(ProjectOut):
    users: Optional[List[UserOut]]


class ProjectWithCustomerOut(ProjectOut):
    customer: CustomerOut


class ProjectWithUsersCustomerOut(ProjectWithUsersOut, ProjectWithCustomerOut):
    pass


class CustomerWithProjectsOut(CustomerOut):
    projects: Optional[List[ProjectOut]]


class CustomerWithProjectsUsersOut(CustomerOut):
    projects: Optional[List[ProjectWithUsersOut]]


class UserWithProjectOut(UserOut):
    project: Optional[ProjectOut]
