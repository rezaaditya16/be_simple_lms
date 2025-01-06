from ninja import Schema
from typing import Optional
from datetime import datetime

from django.contrib.auth.models import User

class UserOut(Schema):
    id: int
    email: str
    first_name: str
    last_name: str


class CourseSchemaOut(Schema):
    id: int
    name: str
    description: str
    price: int
    image: Optional[str]
    teacher: UserOut
    created_at: datetime
    updated_at: datetime


class CourseSchemaIn(Schema):
    name: str
    description: str
    price: int


class CourseMemberOut(Schema):
    id: int
    course_id: CourseSchemaOut
    user_id: UserOut
    roles: str


class CourseContentMini(Schema):
    id: int
    name: str


class CourseContentFull(Schema):
    id: int
    name: str
    description: str


class CourseCommentOut(Schema):
    id: int
    content_id: int
    user_id: UserOut
    comment: str


class CourseCommentIn(Schema):
    comment: str
