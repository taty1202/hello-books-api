from flask import abort, make_response
from ..db import db


def validate_model(cls ,model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 404))
    
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except:
        response = {"message": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add()
    db.session.commit()

    return new_model.to_dict(), 201