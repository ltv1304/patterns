import sqlite3
from abc import ABC, abstractmethod
from dataclasses import make_dataclass

from Framework.apps import Subject
from Framework.exceptions import RecordNotFoundException, DbTableIsEmpty, DbException, DbCommitException, \
    DbUpdateException, DbDeleteException


class AbstractSerializer(ABC, Subject):
    def __init__(self, connection: sqlite3.Connection, table, class_name, fields):
        super(AbstractSerializer, self).__init__()
        self.connection = connection
        self.cursor = connection.cursor()
        self.table = table
        self.class_name = class_name
        self.fields = fields
        self.fields_str = ', '.join(self.fields)
        self.class_fields = ('id',) + fields
        self.class_instance = None

    ############# ФАБРИЧНЫЙ МЕТОД #############################
    @property
    def Class(self):
        return make_dataclass(self.class_name, self.class_fields)

    @abstractmethod
    def data_cook(self, data: str):
        return data

    def save(self, data=None, pk=None, commit=True):
        if type(data) == type(self.class_instance):
            data_dict = {key: val for key, val in zip(self.class_fields, [getattr(data, x) for x in self.class_fields])}
            pk = data.id
            if self.pk_exist(pk):
                self.update(data_dict, pk)
            else:
                self.insert(data_dict)
            self.end_transaction()
            return data
        else:
            data_dict = self.data_cook(data)
            if type(data_dict) == str:
                raise NotImplementedError(
                    f"Model property function don't declared in serializer {self.__class__.__name__}")

            statement = f"BEGIN;"
            self.cursor.execute(statement)

        if pk:
            self.update(data_dict, pk)
        else:
            pk = self.insert(data_dict)

        self.class_instance = self.find_by_id(pk)

        if not commit:
            statement = f"ROLLBACK;"
            self.cursor.execute(statement)
        else:
            self.end_transaction()

        self.class_instance = self.class_instance

        return self.class_instance

    def pk_exist(self, pk):
        statement = f'SELECT EXISTS(SELECT id FROM {self.table} WHERE id = ?)'
        self.cursor.execute(statement, (str(pk), ))
        result = self.cursor.fetchone()[0]
        return bool(result)

    def get_last_id(self):
        statement = f'SELECT MAX(id) FROM {self.table};'
        self.cursor.execute(statement)
        result = self.cursor.fetchone()[0]
        return int(result)

    def end_transaction(self):
        try:
            self.connection.commit()
        except DbException as e:
            raise DbCommitException(e.args)

    def find_by_id(self, pk: int):
        statement = f"SELECT * FROM {self.table} WHERE id=?;"
        self.cursor.execute(statement, (pk,))
        query = self.cursor.fetchone()
        result = self.query2dict(query, self.class_fields)
        if result:
            return self.Class(**result)
        else:
            raise RecordNotFoundException(f'record with id={pk} not found')

    def get_all(self) -> list:
        statement = f"SELECT * FROM {self.table};"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return [self.Class(**self.query2dict(data, self.class_fields)) for data in result]
        else:
            raise DbTableIsEmpty(f'No records in table {self.table}')

    def insert(self, data: dict) -> int:
        pattern = ', '.join(['?' for _ in self.fields])
        statement = f"INSERT INTO {self.table} ({self.fields_str}) VALUES ({pattern});"
        self.cursor.execute(statement, tuple([data[key] for key in self.fields]))
        return self.get_last_id()

    def update(self, data: str, pk: int) -> int:
        statement = f'UPDATE {self.table} SET {", ".join([x + "=?" for x in self.fields])} WHERE id=?;'
        self.cursor.execute(statement, tuple([data[key] for key in self.fields]) + (pk,))
        return pk

    def delete(self, pk: int) -> int:
        statement = f"DELETE FROM {self.table} WHERE id=?;"
        self.cursor.execute(statement, (pk,))
        try:
            self.connection.commit()
        except DbException as e:
            raise DbDeleteException(e.args)
        return pk

    @staticmethod
    def get_data(data: str):
        message_fields = data.split('&')
        message_dict = {}
        for field in message_fields:
            key, val = field.split('=', 1)
            message_dict[key] = val
        return message_dict

    @staticmethod
    def query2dict(query: tuple, fields: tuple):
        result = {}
        for key, val in zip(fields, query):
            result[key] = val
        return result

    def get_foreign_data(self, item, many2many_field, many2many_table, serializer, related_field):
        statement = f"SELECT {many2many_field}_id FROM {many2many_table} WHERE {self.table}_id=?;"
        self.cursor.execute(statement, (item.id,))
        query = self.cursor.fetchall()
        if query:
            for key in query:
                getattr(item, related_field).append(serializer.find_by_id(key[0]))
                # item.course_list.append((key[0]))
        return item

    class RelatedOdjSerializer:

        def find_by_id(self, pk):
            return pk
