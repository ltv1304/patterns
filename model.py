from abc import ABC, abstractmethod
from dataclasses import dataclass


class AbstractFactory(ABC):

    @staticmethod
    def get_data(data):
        message_fields = data.split('&')
        message_dict = {}
        for field in message_fields:
            key, val = field.split('=', 1)
            message_dict[key] = val
        return message_dict


class Category:
    id = 0

    def __init__(self, data):
        self.id = Category.id
        Category.id += 1
        self.name = data['name']


class CategoryFactory(AbstractFactory):
    @classmethod
    def crate(cls, data):
        message_dict = cls.get_data(data)
        return Category(message_dict)


class OfflineCourseFactory:

    @classmethod
    def create(cls, id, data):
        return cls.Course(id, **data)

    @dataclass
    class Course:
        id: int
        name: str
        detail: str
        category: str
        type: str = 'offline'


class OnlineCourseFactory(OfflineCourseFactory):

    @dataclass
    class Course:
        id: int
        name: str
        detail: str
        category: str
        type: str = 'online'


class Fabric(AbstractFactory):
    ONLINE = 'online'
    OFFLINE = 'offline'
    id = 0

    @classmethod
    def create_course(cls, data):
        message_dict = cls.get_data(data)

        if message_dict['type'] == cls.ONLINE:
            return OnlineCourseFactory.create(cls.id, message_dict)
        elif message_dict['type'] == cls.OFFLINE:
            return OfflineCourseFactory.create(cls.id, message_dict)

        cls.id += 1

