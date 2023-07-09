# Предварительное наполнение БД примерами.
# Перед тем, как убирать из проекта, надо убдиться, что весь код адекватно реагирует на пустые таблицы

from utils import hash_id, list_to_string, list_to_string2

from model import DataBase, Questionnaire, Chapter, Question
from misc import DATABASE_URL


db = DataBase(db_name=DATABASE_URL)

example_question1 = Question(text='Какой показатель выбран в качестве целевой переменной модели? Как обосновывается выбор данного показателя разработчиком? Насколько логично это обоснование?', is_obligatory=1)
example_question2 = Question(text='Тут у нас тупо текст, вообще даже не вопрос', is_obligatory=0)
example_question3 = Question(text='А что за раздел-то там был? ыва', is_obligatory=1)
example_questions = [example_question1, example_question2, example_question3]

eq_hash1 = hash_id([example_question1.text, example_question1.is_obligatory])
eq_hash2 = hash_id([example_question2.text, example_question2.is_obligatory])
eq_hash3 = hash_id([example_question3.text, example_question3.is_obligatory])

print('eq_hash1: ', eq_hash1)

f = list_to_string2([eq_hash1,eq_hash2])

print('f: ', f)

example_chapter1 = Chapter(text='Целевая переменная', id_questions_string=f)
example_chapter2 = Chapter(text='Методология?', id_questions_string=list_to_string2([eq_hash3]))
example_chapters = [example_chapter1, example_chapter2]

ff= list_to_string2([hash_id([example_chapter1.text, example_chapter1.id_questions]),hash_id([example_chapter2.text, example_chapter2.id_questions])] )

example_questionnaire1 = Questionnaire(name='Нормальный опросник', version=1, author='Илья Ханьков', id_chapters_string=ff)
example_questionnaires = [example_questionnaire1]

for question in example_questions:
    db.add_question(question)

for chapter in example_chapters:
    db.add_chapter(chapter)

for questionnaire in example_questionnaires:
    db.add_questionnaire(questionnaire)

