from flask import render_template, request
from app import app
from app.forms import BookDetails
from app.models import Book


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

        list_of_books = Book().retrieve()

        return render_template('index.html', book_list=list_of_books)


@app.route('/Book_Details', methods=['POST', 'GET'], defaults={'book_id': None})
@app.route('/Book_Details/<int:book_id>', methods=['POST', 'GET'])
def Book_Details(book_id):

    form = None

    if book_id is not None:
        book_details = Book().retrieve(book_id)
        form = BookDetails().populate_form(book_details)
    else:
        form = BookDetails()

    if request.method == 'POST' and form.validate_on_submit():

        return render_template('book_details.html', form=form)
    else:
        return render_template('book_details.html', form=form)


@app.route('/Book_lookup', methods=['POST', 'GET'])
def Book_lookup():
    pass
