from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description
    
    def to_dict(self):
        return dict(
                id=self.id,
                title=self.title,
                description=self.description
            
        )

# books = [
#     Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
#     Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]