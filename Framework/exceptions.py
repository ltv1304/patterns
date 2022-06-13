class DbException(Exception): pass
class RecordNotFoundException(DbException): pass
class DbUpdateException(DbException): pass
class DbCommitException(DbException): pass
class DbDeleteException(DbException): pass
class DbTableIsEmpty(DbException): pass


class Http405Error(Exception): pass
class Http404Error(Exception): pass