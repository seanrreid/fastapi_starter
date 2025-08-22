from .base import Base


class Stuff(Base, table=True):
    __tablename__ = "stuff"

    # some parameters for the Stuff model
    # examples might be...
    title: str
    description: str
