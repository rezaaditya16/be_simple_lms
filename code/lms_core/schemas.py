from ninja import Schema
from typing import List, Optional
from datetime import datetime

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

class ContentCompletionSchemaIn(Schema):
    content_id: int
    user_id: int

class ContentCompletionSchemaOut(Schema):
    id: int
    content_id: int
    user_id: int
    completed_at: datetime

class ProfileSchemaIn(Schema):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    description: Optional[str]
    profile_picture: Optional[str]

class ProfileSchemaOut(Schema):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    description: Optional[str]
    profile_picture: Optional[str]
    courses_created: List[CourseSchemaOut]
    courses_enrolled: List[CourseMemberOut]