from flask import Blueprint, abort, make_response
from app.models.book import books


books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.get("")
def get_all_books():
    books_response = []
    for book in books:
        books_response.append(book.to_book())
    return books_response

@books_bp.get("/<book_identifier>")
def get_one_book(book_identifier):
    book = validate_book_identifier(book_identifier)
    return book.to_book(book_identifier)

def validate_book_identifier(book_identifier):
    if book_identifier.isdigit():
        return validate_book_id(book_identifier)
    else:
        return validate_book_name(book_identifier)
    
def validate_book_id(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"book id {book_id} invalid"}, 400))

    for book in books:
        if book.id == book_id:
            return book
    abort(make_response({"message": f"book id {book_id} invalid"}, 404))


def validate_book_name(book_name):
    for book in books:
        if book.name.lower() == book_name.lower():
            return book
    abort(make_response({"message": f"book id {book_name} invalid"}, 404))
