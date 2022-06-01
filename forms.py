from Framework.forms import Forms
from model import Course, Category


class CourseForm(Forms):
    def __init__(self, data):
        message_fields = data.split('&')
        self.message_dict = {}
        for field in message_fields:
            key, val = field.split('=', 1)
            self.message_dict[key] = val

    def create(self):
        Course.create(**self.message_dict)


class CategoryForm(Forms):
    def __init__(self, data):
        message_fields = data.split('&')
        self.message_dict = {}
        for field in message_fields:
            key, val = field.split('=', 1)
            self.message_dict[key] = val

    def create(self):
        Category.create(**self.message_dict)