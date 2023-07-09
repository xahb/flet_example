# 3rd
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy import UniqueConstraint

from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from utils import list_to_string, hash_id, list_to_string2

from misc import DATABASE_URL

Base = declarative_base()


class Questionnaire(Base):
    __tablename__ = 'Questionnaires'
    id = Column(String, primary_key=True)
    id_successor = Column(Integer)
    name = Column(String)
    version = Column(Integer)
    author = Column(String)
    created = Column(DateTime)
    id_chapters = Column(String)

    def __init__(self, name, version, author, id_chapters_string):
        self.id_chapters = id_chapters_string
        #self.id_chapters = re.sub("[{}' ]", "", id_chapters_string).split(',') # (x__x)
        self.id = hash_id([name, version, self.id_chapters])
        self.id_successor = None
        self.name = name
        self.version = version
        self.author = author
        self.created = datetime.now()

    def get_id_chapters(self):
        import re
        return re.sub("[{}' ]", "", self.id_chapters).split(',')
    
    def set_id_chapters(self, lst):
        self.id_chapters = list_to_string2(lst)


class Chapter(Base):
    __tablename__ = 'Chapters'
    id = Column(String, primary_key=True)
    text = Column(String)
    id_questions = Column(String)

    def __init__(self, text, id_questions_string):
        self.id_questions = id_questions_string
        #self.id_questions = re.sub("[{}' ]", "", id_questions_string).split(',')
        self.id = hash_id([text, self.id_questions])
        self.text = text

    def get_id_questions(self):
        import re
        return re.sub("[{}' ]", "", self.id_questions).split(',')

    def set_id_questions(self, lst):
        self.id_questions = list_to_string2(lst)

class Question(Base):
    __tablename__ = 'Questions'
    id = Column(String, primary_key=True)
    text = Column(String)
    is_obligatory = Column(Integer)

    def __init__(self, text, is_obligatory):
        self.id = hash_id([text, is_obligatory])        
        self.text = text
        self.is_obligatory = is_obligatory


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
        questionnaire_chapterlist = questionnaire.get_id_chapters()
        print(questionnaire_chapterlist)
        chapters = self.session.query(Chapter).filter(Chapter.id.in_(questionnaire_chapterlist))#.order_by("order")

        full_chapters = {}
        for chapter in chapters: 
            full_chapters[chapter] = self.session.query(Question).filter(Question.id.in_(chapter.get_id_questions()))#.order_by("order") 

        return {'questionnaire':questionnaire, 'chapters':full_chapters}
    
    def add_questionnaire(self, new_questionnaire):
        self.session.add(new_questionnaire)
        self.session.commit()

    def add_chapter(self, new_chapter):
        self.session.add(new_chapter)
        self.session.commit()

    def add_question(self, new_question):
        self.session.add(new_question)
        self.session.commit()

