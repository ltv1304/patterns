import abc


class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self.subject = None

    @abc.abstractmethod
    def update(self, arg):
        pass


class Subject:
    def __init__(self):
        self._observers = set()
        self._subject_state = self

    def attach(self, observer):
        observer.subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer.subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self)


class SMSNotifier(Observer):
    def update(self, course):
        for student in course:
            print(f'SMS notify {student.name} about changes in {course.name} course')


class EmailNotifier(Observer):
    def update(self, course):
        for student in course:
            print(f'Email notify {student.name} about changes in {course.name} course')