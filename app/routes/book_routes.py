from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from .route_utilities import validate_model
from ..db import db


books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    request_body = request.get_json()
    
    try:
        new_book = Book.from_dict(request_body)
    except KeyError as e:
        response = {"message": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_book)
    db.session.commit()

    response = new_book.to_dict()
    return response, 201

@books_bp.get("")
def get_all_books():
    query = db.select(Book)

    title_param  = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))
    
    query = query.order_by(Book.id)

    books = db.session.scalars(query)

    books_response = [book.to_dict() for book in books]
    return books_response

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    
    return book.to_dict()

@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    # return "", 204
    return Response(status=204, mimetype='application/json')

@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(book_id) 
    db.session.delete(book)
    db.session.commit()

    # return "", 204
    return Response(status=204, mimetype='application/json')
