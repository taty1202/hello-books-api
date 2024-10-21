from flask import Blueprint
from app.models.book import books
from flask import Blueprint, abort, make_response

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.get("")
def get_all_books():
    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return books_response

@books_bp.get("/<book_identifier>")
def get_one_book(book_identifier):
    book = validate_book_identifier(book_identifier)

    return {
        "id":book.id,
        "title":book.title,
        "description":book.description
    }

def validate_book_identifier(book_identifier):
    if book_identifier.isdigit():
        return validate_book_id(book_identifier)
    else:
        return validate_book_name(book_identifier)
    
def validate_book_id(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"book {book_id} invalid"}
        abort(make_response(response, 400))

    for book in books:
        if book.id == book_id:
            return book
    response = {"message": f"book {book_id} not found"}
    abort(make_response(response, 404))

def validate_book_name(book_name):
    for book in books:
        if book.name.lower() == book_name.lower():
            return book
    response = {"message": f"book {book_name} not found"}
    abort(make_response(response, 404))