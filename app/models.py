from app import db, SQLAlchemyError


# many to many tables

BookAuthor = db.Table('book_author', db.metadata,
                      db.Column('book_id', db.Integer, db.ForeignKey('book.book_id')),
                      db.Column('author_id', db.Integer, db.ForeignKey('author.author_id'))
                      )

BookSubject = db.Table('book_subject', db.metadata,
                       db.Column('book_id', db.Integer, db.ForeignKey('book.book_id')),
                       db.Column('subject_id', db.Integer, db.ForeignKey('subject.subject_id'))
                       )


#  Class to add, update and delete data via SQLALchemy sessions
class CRUD():

    def __init__(self):

        self.table_name = None

    def _add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def _update(self):
        return db.session.commit()

    def _delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

    def retrieve(self, id=None):

        try:
            if id is not None:
                result = db.session.query(self.__class__).get(id)
                return result
            else:
                result = db.session.query(self.__class__).all()
                return result

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': e,
                    'code': 500}

    def change_status(self, id, value):

            try:
                result = self.table_name().retrieve(id)
                if result:
                    result.active = value.upper()
                    result._update()
                    return {'code': 200,
                            'msg': '{0} status has been updated'.format(str(self.__class__.__name__))}
                else:
                    return {'code': 200,
                            'msg': '{0} does not exist'.format(str(self.__class__.__name__))}
            except SQLAlchemyError as e:
                print(e)
                db.session.rollback()
                return {'msg': e,
                        'code': 500}

    def update(self, id, data_dict):

        try:
            result = self.table_name().retrieve(id)
            if result:
                for key, value in data_dict.items():
                    setattr(self.__class__, key, value)
                result._update()
                return {'code': 200,
                        'msg': '{0} updated'.format(str(self.__class__.__name__))}
            else:
                return {'code': 200,
                        'msg': '{0} does not exist'.format(str(self.__class__.__name__))}
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {'msg': e,
                    'code': 500}

    def delete_record(self, id):

        try:
            result = self.retrieve(id)

            if result:
                result._delete(result)

                return {'code': 200,
                        'msg': '{0} Deleted'.format(str(self.__class__.__name__))}
            else:
                return {'code': 200,
                        'msg': '{0} does not exist'.format(str(self.__class__.__name__))}

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {'msg': e,
                    'code': 500}

    def add_record(self):
        pass


class BookIsbn(db.Model):
    __tablename__ = 'book_isbn'

    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
    isbn_type_id = db.Column(db.Integer, db.ForeignKey('isbn_type.isbn_type_id'), primary_key=True)
    value = db.Column(db.VARCHAR(30))
    book = db.relationship('Book')
    isbn_type = db.relationship('IsbnType', backref='book_isbn')


class IsbnType(db.Model, CRUD):

    __tablename__ = "isbn_type"

    isbn_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn_type_name = db.Column(db.VARCHAR(50))
    active = db.Column(db.CHAR(1), server_default='Y')

    books = db.relationship("BookIsbn")

    sqlite_autoincrement = True

    @staticmethod
    def search(lookup):
        try:
            result = db.session.query(IsbnType)\
                               .filter(IsbnType.isbn_type_name.like("%" + str(lookup) + "%"))\
                               .filter(IsbnType.active == 'Y')\
                               .all()
            return result
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {'code': -1,
                    'msg': e}


class Publisher(db.Model, CRUD):

    __tablename__ = "publisher"

    publisher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publisher_name = db.Column(db.VARCHAR(100))
    publisher_code = db.Column(db.VARCHAR(50))
    active = db.Column(db.CHAR(1), server_default='Y')

    sqlite_autoincrement = True

    @staticmethod
    def search(lookup):
        try:
            result = db.session.query(Publisher)\
                               .filter(db.or_(Publisher.publisher_name.like("%" + str(lookup) + "%"),
                                              Publisher.publisher_code.like("%" + str(lookup) + "%")))\
                               .all()
            return result

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {'msg': e,
                    'code': 500}

    def add(self, name, code):
        try:

            if not Publisher.search(code):

                publisher = Publisher(publisher_name=name, publisher_code=code)

                publisher._add(publisher)

                return {'code': 201,
                        'msg': 'Success'}

            else:

                return {'code': 200,
                        'msg': 'Publisher already exists'}

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {'msg': e,
                    'code': 500}


class Author(db.Model, CRUD):

    __tablename__ = "author"

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.VARCHAR(100))
    author_code = db.Column(db.VARCHAR(50))
    active = db.Column(db.CHAR(1), server_default='Y')

    sqlite_autoincrement = True

    @staticmethod
    def search(lookup):
        try:
            result = db.session.query(Author)\
                               .filter(db.or_(Author.author_name.like("%" + str(lookup) + "%"),
                                              Author.author_code.like("%" + str(lookup) + "%")))\
                               .all()
            return result

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {'msg': e,
                    'code': 500}

    def add(self, name, code):
        try:

            if not Author.search(code):

                author = Author(author_name=name, author_code=code)

                author._add(author)

                return {'code': 201,
                        'msg': 'Success'}

            else:

                return {'code': 200,
                        'msg': 'Author already exists'}

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {'msg': e,
                    'code': 500}


class Subject(db.Model, CRUD):

    __tablename__ = "subject"

    subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.VARCHAR(100))
    subject_code = db.Column(db.VARCHAR(50))
    active = db.Column(db.CHAR(1), server_default='Y')

    sqlite_autoincrement = True

    @staticmethod
    def search(lookup):
        try:
            result = db.session.query(Subject)\
                               .filter(db.or_(Subject.subject_name.like("%" + str(lookup) + "%"),
                                              Subject.subject_code.like("%" + str(lookup) + "%")))\
                               .all()
            return result

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {'msg': e,
                    'code': 500}

    def add(self, name, code):
        try:

            if not Subject.search(code):

                subject = Subject(subject_name=name, subject_code=code)

                subject._add(subject)

                return {'code': 201,
                        'msg': 'Success'}

            else:

                return {'code': 200,
                        'msg': 'Subject already exists'}

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {'msg': e,
                    'code': 500}


class Book(db.Model, CRUD):

    __tablename__ = "book"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.VARCHAR(100))
    page_count = db.Column(db.Integer)
    year = db.Column(db.Integer)
    synopsis = db.Column(db.VARCHAR(500))
    dewey_normal = db.Column(db.VARCHAR(20))
    dewey_decimal = db.Column(db.VARCHAR(20))
    # cover_url_sm = db.Column(db.VARCHAR(500))
    # cover_url_l = db.Column(db.VARCHAR(500))

    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.publisher_id'))
    publisher = db.relationship('Publisher',  backref='book')
    # manay to many relationships
    isbn = db.relationship('BookIsbn', cascade='all')
    subject = db.relationship('Subject', secondary=BookSubject, backref='book')
    author = db.relationship('Author', secondary=BookAuthor, backref='book')

    sqlite_autoincrement = True

    def add(self, book_obj):
        try:
            result = self.retrieve()
            if result:
                # isbn_values = BookIsbn(book_obj['isbn'][0])
                # book = Book(Book.title=book_obj['title'], Book.page_count=book_obj['page_count'])
                book = Book(title=book_obj['title'], page_count=book_obj['page_count'])
                author = Author().retrieve(1)
                book.author.append(author)
                book._add(book)
                return {'code': 200,
                        'msg': '{0} added'.format(str(self.__class__.__name__)),
                        'data': book.book_id}
            else:
                return {'code': 500,
                        'msg': '{0} already exists'.format(str(self.__class__.__name__))}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'msg': e,
                    'code': 500}

    @staticmethod
    def search():
        raise NotImplemented()
        # try:
        #     pass

        # except SQLAlchemyError as e:
        #     print(e)
        #     db.session.rollback()
        #     return {'msg': e,
        #             'code': 500}

    def update(self):
        raise NotImplemented()


db.create_all()
