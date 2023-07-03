# 3rd
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

from misc import DATABASE_URL

Base = declarative_base()


class Questionnaire(Base):
    __tablename__ = 'Questionnaires'
    id = Column(Integer, primary_key=True)
    id_successor = Column(Integer)
    name = Column(String)
    version = Column(Integer)
    author = Column(String)
    created = Column(DateTime)


class Chapter(Base):
    __tablename__ = 'Chapters'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    id_questionnaire = Column(Integer)


# эта штука нужна для создания нового раздела
class DummyChapter():
    def __init__(self, id, text, id_questionnaire):
        self.id = id
        self.text = text
        self.id_questionnaire = id_questionnaire


class Question(Base):
    __tablename__ = 'Questions'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_obligatory = Column(Integer)
    id_chapter = Column(Integer)
    id_questionnaire = Column(Integer)


# эта штука нужна для создания нового раздела
class DummyQuestion():
    def __init__(self, id, text, is_obligatory, id_chapter, id_questionnaire):
        self.id = id
        self.text = text
        self.is_obligatory = is_obligatory
        self.id_chapter = id_chapter
        self.id_questionnaire = id_questionnaire


class DataBase:
    def __init__(self, db_name: str) -> None:
        """This class will configure our database."""
        engine = create_engine(db_name)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        self.session = Session()

    def select_questionnaries_table(self):
        return self.session.query(Questionnaire).all()
    
    def select_questionnaire_by_id(self, ext_id):
        questionnaire = self.session.query(Questionnaire).filter_by(id = ext_id).first()
        chapters = self.session.query(Chapter).filter_by(id_questionnaire = ext_id)
        questions = self.session.query(Question).filter_by(id_questionnaire = ext_id)

        full_chapters = {} #[setattr(chapter, "Questions", [question for question in questions if question.id_chapter == chapter.id]) for chapter in chapters]
        for chapter in chapters: 
            full_chapters[chapter] = [question for question in questions if question.id_chapter == chapter.id]

        #if questionnaire is not None:
            #questionnaire.chapters = full_chapters
            #setattr(questionnaire, 'chapters', full_chapters)

        return {'questionnaire':questionnaire, 'chapters':full_chapters} #{'Questionnaire':questionnaire, 'Chapters':chapters, 'Questions':questions}

