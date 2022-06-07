from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from Framework.apps import Subject


class AbstractFactory(ABC):

    @staticmethod
    def get_data(data):
        message_fields = data.split('&')
        message_dict = {}
        for field in message_fields:
            key, val = field.split('=', 1)
            message_dict[key] = val
        return message_dict


class Student:
    id = 0

    def __init__(self, data):
        self.id = Student.id
        Student.id += 1
        self.name = data['name']
        self.course_list = []

    def manage_course(self, course):
        self.course_list = course


class StudentFactory(AbstractFactory):
    @classmethod
    def crate(cls, data):
        message_dict = cls.get_data(data)
        return Student(message_dict)


class Category:
    id = 0

    def __init__(self, data):
        self.id = Category.id
        Category.id += 1
        self.name = data['name']
        self.course_list = []

    def __getitem__(self, item):
        return self.course_list[item]


class CategoryFactory(AbstractFactory):
    @classmethod
    def crate(cls, data):
        message_dict = cls.get_data(data)
        return Category(message_dict)


@dataclass
class CourseRaw(Subject):
    id: int
    name: str
    detail: str
    category: int
    student_list: List = field(default_factory=list)

    def __post_init__(self):
        super().__init__()

    def __getitem__(self, item):
        return self.student_list[item]


class OfflineCourseFactory:

    @classmethod
    def create(cls, id, data):
        return cls.Course(id, **data)

    @dataclass
    class Course(CourseRaw):
        type: str = 'offline'


class OnlineCourseFactory(OfflineCourseFactory):

    @dataclass
    class Course(CourseRaw):
        type: str = 'online'


class Fabric(AbstractFactory):
    ONLINE = 'online'
    OFFLINE = 'offline'
    id = 0

    @classmethod
    def create_course(cls, data):
        message_dict = cls.get_data(data)
        message_dict['category'] = int(message_dict['category'])
        if message_dict['type'] == cls.ONLINE:
            course = OnlineCourseFactory.create(cls.id, message_dict)
        elif message_dict['type'] == cls.OFFLINE:
            course = OfflineCourseFactory.create(cls.id, message_dict)

        cls.id += 1
        return course

    @classmethod
    def change_course(cls, course, data):
        message_dict = cls.get_data(data)
        message_dict['category'] = int(message_dict['category'])
        for key, val in message_dict.items():
            course.__setattr__(key, val)
        course._notify()



