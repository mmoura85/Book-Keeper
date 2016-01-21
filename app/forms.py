from flask.ext.wtf import Form
from wtforms import SubmitField, SelectField, TextField, TextAreaField, HiddenField
from app.models import Author, Publisher, IsbnType


class IsbnSelection(Form):
    isbn_selection = SelectField('ISBN', choices=[(row.isbn_type_id, row.isbn_type_name) for row in IsbnType().retrieve()], coerce=int)


class AuthorSelection(Form):
    author_selection = SelectField('Author', choices=[(row.author_id, row.author_name) for row in Author().retrieve()], coerce=int)


class PublisherSelection(Form):
    publisher_selection = SelectField('Publisher', choices=[(row.publisher_id, row.publisher_name) for row in Publisher().retrieve()], coerce=int)


class BookDetails(AuthorSelection, PublisherSelection, IsbnSelection):
    book_id = HiddenField('book_id')
    save = SubmitField('Save')
    title = TextField('Title')
    page_count = TextField('Page Count')
    year = TextField('Year')
    synopsis = TextAreaField('Synopsis')
    authors = TextAreaField('Authors')
    publishers = TextAreaField('Publishers')
    dewey_normal = TextField('Dewey Normal')
    dewey_decimal = TextField('Dewey Decimal')
    isbn_lookup = TextAreaField('ISBN')

    def __init__(self):
        super(BookDetails, self).__init__()

    @classmethod
    def populate_form(cls,  data):
        form = cls()
        return form
