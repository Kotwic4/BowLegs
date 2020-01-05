import enum

from sqlalchemy import Column, Text, Enum

from database import Base


class Status(enum.Enum):
    TODO = "TODO"
    DONE = "DONE"


class Picture(Base):
    __tablename__ = 'pictures'
    id = Column(Text, primary_key=True)
    input_path = Column(Text)
    mask_path = Column(Text)
    result_path = Column(Text)
    status = Column(Enum(Status))

    def __init__(self, id, input_path, mask_path=None, result_path=None):
        self.id = id
        self.input_path = input_path
        self.mask_path = mask_path
        self.result_path = result_path
        self.status = Status.TODO

    def __repr__(self):
        return '<Picture %r>' % self.id
