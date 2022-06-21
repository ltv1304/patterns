import sqlite3

from Framework.apps import Subject, EmailNotifier, SMSNotifier
from Framework.exceptions import DbException, DbUpdateException, Http500Error
from Framework.serializers import AbstractSerializer


class CategorySerializer(AbstractSerializer):
    def __init__(self, *args):
        super().__init__(*args)

    def get_all(self):
        try:
            data = super(CategorySerializer, self).get_all()
        except DbException:
            data = []
        return data

    def data_cook(self, data: str):
        data_dict = self.get_data(data)
        data_dict['name'] = data_dict['name'].rstrip()
        return data_dict


class CourseBaseSerializer(AbstractSerializer):
    def __init__(self, *args):
        super().__init__(*args)

    def get_all(self):
        try:
            course_list = super(CourseBaseSerializer, self).get_all()
        except DbException:
            course_list = []
        return course_list

    def data_cook(self, data: str):
        data_dict = self.get_data(data)
        data_dict['name'] = data_dict['name'].rstrip()
        data_dict['detail'] = data_dict['detail'].rstrip()
        data_dict['detail'] = int(data_dict['detail'])
        return data_dict


class CourseSerializer(AbstractSerializer):
    def __init__(self, *args):
        super().__init__(*args)
        self.many2many_table = 'course_student'
        self.many2many_field = 'student'
        self.student_serializer = StudentBaseSerializer(conn, 'student', 'Fabric', ('name',))
        self.related_field = 'students_list'


    @property
    def Class(self):
        super_class = super(CourseSerializer, self).Class
        related_field = self.related_field

        class _Class(super_class):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.__dict__[related_field] = []

            def __getitem__(self, item):
                return self.students_list[item]

            def __contains__(self, item):
                for student in self.students_list:
                    if student.id == item.id:
                        return True
                return False

        return _Class

    def get_all(self):
        try:
            course_list = super(CourseSerializer, self).get_all()
        except DbException:
            course_list = []
        if course_list:
            result = []
            for course in course_list:
                result.append(self.get_foreign_data(course,
                                                    self.many2many_field,
                                                    self.many2many_table,
                                                    self.student_serializer,
                                                    self.related_field))
        return course_list

    def find_by_id(self, pk: int):
        course = super(CourseSerializer, self).find_by_id(pk)
        if course:
            course = self.get_foreign_data(course,
                                            self.many2many_field,
                                            self.many2many_table,
                                            self.student_serializer,
                                            self.related_field)
        return course

    def data_cook(self, data: str):
        data_dict = self.get_data(data)
        data_dict['name'] = data_dict['name'].rstrip()
        data_dict['detail'] = data_dict['detail'].rstrip()
        data_dict['category'] = int(data_dict['category'])
        return data_dict

    def update(self, *args):
        super(CourseSerializer, self).update(*args)
        self._subject_state = self.find_by_id(args[1])
        self._notify()


class StudentBaseSerializer(AbstractSerializer):
    def __init__(self, *args):
        super().__init__(*args)

    def get_all(self):
        try:
            student_list = super(StudentBaseSerializer, self).get_all()
        except DbException:
            student_list = []
        return student_list

    def data_cook(self, data: str):
        data_dict = self.get_data(data)
        data_dict['name'] = data_dict['name'].rstrip()
        return data_dict


class StudentSerializer(AbstractSerializer):
    def __init__(self, *args):
        super().__init__(*args)
        self.many2many_table = 'course_student'
        self.course_serializer = CourseBaseSerializer(conn, 'course', 'Fabric', ('name',))
        self.many2many_field = 'course'
        self.related_field = 'course_list'

    @property
    def Class(self):
        super_class = super(StudentSerializer, self).Class
        related_field = self.related_field

        class _Class(super_class):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.__dict__[related_field] = []

            def __getitem__(self, item):
                return self.course_list[item]

            def __contains__(self, item):
                for course in self.course_list:
                    if course.id == item.id:
                        return True
                return False

        return _Class

    def update(self, data: str, pk: int):
        statement = f"SELECT * FROM {self.many2many_table} WHERE student_id=?;"
        self.cursor.execute(statement, (pk,))
        query = self.cursor.fetchall()
        if query:
            statement = f"DELETE FROM {self.many2many_table} WHERE student_id=?;"
            self.cursor.execute(statement, (pk,))

        statement = f"INSERT INTO {self.many2many_table} (course_id, student_id) VALUES (?, ?);"
        for course_id in data:
            self.cursor.execute(statement, (course_id, pk))
        try:
            self.connection.commit()
        except DbException as e:
            raise DbUpdateException(e.args)

    def get_all(self):
        try:
            student_list = super(StudentSerializer, self).get_all()
        except DbException:
            student_list = []
        if student_list:
            result = []
            for student in student_list:
                result.append(self.get_foreign_data(student,
                                                    self.many2many_field,
                                                    self.many2many_table,
                                                    self.course_serializer,
                                                    self.related_field))
        return student_list

    def find_by_id(self, pk: int):
        student = super(StudentSerializer, self).find_by_id(pk)
        if student:
            student = self.get_foreign_data(student,
                                            self.many2many_field,
                                            self.many2many_table,
                                            self.course_serializer,
                                            self.related_field)
        return student

    # Плохая реализация цепочки ответственности
    def data_cook(self, data: str):
        try:
            result = self.student_data_cook(data)
        except Exception:
            try:
                result = self.course_data_cook(data)
            except Exception:
                raise Http500Error
        return result

    def student_data_cook(self, data: str):
        data_dict = self.get_data(data)
        data_dict['name'] = data_dict['name'].rstrip()
        return data_dict

    @staticmethod
    def course_data_cook(data: str):
        message_fields = data.split('&')
        course_list = []
        for field in message_fields:
            key, val = field.split('=', 1)
            course_list.append(val)
        return course_list


conn = sqlite3.connect('test.db')
category_serializer = CategorySerializer(conn, 'category', 'Category', ('name', ))
course_serializer = CourseSerializer(conn, 'course', 'Fabric', ('name', 'detail', 'category', 'type'))
course_serializer.attach(SMSNotifier())
course_serializer.attach(EmailNotifier())
student_serializer = StudentSerializer(conn, 'student', 'Student', ('name', ))
