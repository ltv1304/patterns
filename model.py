from peewee import *

db = SqliteDatabase('univer.db')


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField()

    class Meta:
        db_table = 'category'


class Course(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100, unique=True)
    type = CharField(max_length=100)
    detail = CharField(max_length=100)
    category = ForeignKeyField(Category, related_name='category_details')

    class Meta:
        db_table = 'course'


class Student(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100, unique=True)


class StudentCourse(BaseModel):
    student = ForeignKeyField(Student)
    course = ForeignKeyField(Course)


