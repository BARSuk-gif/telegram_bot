import sqlalchemy as sq
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = sq.Column(sq.BigInteger, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    count_words = sq.Column(sq.Integer, nullable=False)

<<<<<<< HEAD

=======
  
>>>>>>> 0e16db93ae660c7660190968e7464c401da9c2e9
class Target_words(Base):
    __tablename__ = "target_words"

    id = sq.Column(sq.Integer, primary_key=True)
    target_word = sq.Column(sq.String(length=40), nullable=False)
    user_id = sq.Column(sq.BigInteger, sq.ForeignKey("users.id"))
    created_by = sq.Column(sq.String(length=40))

    users = relationship(Users, backref="target_words")


class Translate_words(Base):
    __tablename__ = "translate_words"

    id = sq.Column(sq.Integer, primary_key=True)
    translate_word = sq.Column(sq.String(length=40), nullable=False)
    target_id = sq.Column(sq.Integer, sq.ForeignKey("target_words.id"))

    target_words = relationship(Target_words, backref="translate_words")


class Others_words(Base):
    __tablename__ = "others_words"

    id = sq.Column(sq.Integer, primary_key=True)
    other_word = sq.Column(sq.String(length=40), nullable=False)
    target_id = sq.Column(sq.Integer, sq.ForeignKey("target_words.id"))

    target_words = relationship(Target_words, backref="others_words")


class User_Target_Relations(Base):
    __tablename__ = "user_target_relations"

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.BigInteger, sq.ForeignKey("users.id"))
    target_id = sq.Column(sq.Integer, sq.ForeignKey("target_words.id"))
    is_active = sq.Column(sq.BOOLEAN)


# def create_tables(engine):
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)

