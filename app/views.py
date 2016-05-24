from flask import render_template, request
from app import app
from app.forms import BookDetails
from app.models import Book


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    list_of_books = Book().retrieve()
    return render_template('index.html', book_list=list_of_books)


@app.route('/book_details/<int:book_id>', methods=['GET'])
@app.route('/index/book_details/<int:book_id>', methods=['GET'])
def Book_Details(book_id):

    form = BookDetails()
    book_details = Book().retrieve(book_id)
    return render_template('book_details.html', form=form, book_details=book_details)


@app.route('/book_edit', methods=['POST'], defaults={'book_id': None})
@app.route('/book_edit/<int:book_id>', methods=['POST'])
def Book_edit(book_id):

    form = None

    if request.method == 'POST' and form.validate_on_submit():

        form = BookDetails()

        if book_id is not None:
            book_details = Book().retrieve(book_id)
            form.populate_form(book_details)

        # response = Book.add()
    elif book_id is None:
        # response = Book.update()
        pass

        return render_template('book_details.html', form=form)


@app.route('/Book_lookup', methods=['POST', 'GET'])
def Book_lookup():
    form = BookDetails()
    if request.method == 'POST' and form.validate_on_submit():
        # print(form.data)
        return render_template('/book_form.html', form=form)
    else:
        return render_template('/book_form.html', form=form)
