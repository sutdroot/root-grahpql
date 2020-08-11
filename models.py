from database import Base
from sqlalchemy import Column, String, Integer, DateTime


class Feedback(Base):
    __tablename__ = 'feedback'

    fbid = Column(Integer, primary_key=True)
    address = Column(String)
    name = Column(String)
    email = Column(String)
    message = Column(String)
    created = Column(DateTime)

    def __init__(self, address, name, email, message, created):
        self.address = address
        self.name = name
        self.email = email
        self.message = message
        self.created = created

    def update(self, *args):
        args = args[0]

        for key, value in args.items():
            setattr(self, key, value)
