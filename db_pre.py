# Предварительное наполнение БД примерами.
# Перед тем, как убирать из проекта, надо убдиться, что весь код адекватно реагирует на пустые таблицы

from model import DataBase, Questionnaire, Chapter, Question
from misc import DATABASE_URL

db = DataBase(db_name=DATABASE_URL)

example_questionnaire = Questionnaire(name='Нормальный опросник', version=1, author='Илья Ханьков', id_chapters='')
example_chapter = Chapter(text='Целевая переменная', id_questionnaire=1, order=1)
example_question = Question(text='Какой показатель выбран в качестве целевой переменной модели? Как обосновывается выбор данного показателя разработчиком? Насколько логично это обоснование?', is_obligatory=1, id_chapter=1, id_questionnaire=1)

db.add_questionnaire(example_questionnaire)
db.add_chapter(example_chapter)
db.add_question(example_question)



