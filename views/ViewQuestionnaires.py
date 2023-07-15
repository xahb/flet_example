import flet as ft
from misc import qq

from misc import DATABASE_URL

from model import DataBase
from model import Questionnaire, Chapter, Question
from utils import hash_id, list_to_string2

from styles import HeadlineStyle, SubHeadlineStyle

def ViewQuestionnaires(page, bar, rail):

    class RenderedQuestionnairesTable(ft.UserControl):

        def __init__(self, select_questionnaires):
            super().__init__()
            self.select_questionnaires = select_questionnaires
            self.column_names = ['Опросник', 'Автор', 'Дата создания']

        def build(self):
            columns = [ft.DataColumn(ft.Text(x)) for x in self.column_names]
            rows = []
            for questionnaire in self.select_questionnaires:
                row = ft.DataRow(cells=[ft.DataCell(ft.ElevatedButton(f"{questionnaire.name} - вер. {questionnaire.version}")),
                                        ft.DataCell(ft.Text(questionnaire.author)),
                                        ft.DataCell(ft.Text(questionnaire.created))
                                        ]
                                )
                rows.append(row)
            return ft.DataTable(columns, rows)
                           
   
    class RenderedQuestion(ft.UserControl):

        def __init__(self, rank, text, obligatory, delete_question):
            super().__init__()
            self.annotation = ft.Text(f"Вопрос {rank}:", width=150, size=15, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
            self.text = ft.TextField(multiline=True, value= text, border=ft.InputBorder.UNDERLINE, width=600)
            self.is_obligatory = ft.Checkbox(label="Обязательный", value=obligatory, width=150)
            self.button_delete = ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color="pink600", icon_size=30, tooltip="Удалить вопрос", on_click=self.delete_self)
            self.delete_question = delete_question

        def build(self):
            return ft.Card(ft.Row(controls=[self.annotation, self.text, self.is_obligatory, self.button_delete]), width=1000)
        
        def delete_self(self, e):
            self.delete_question(self)

        def update_rank(self, new_rank):
            self.annotation = ft.Text(f"Вопрос {new_rank}:", width=150, size=15, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)


    class RenderedChapter(ft.UserControl):

        def __init__(self, chapter, rank, questions_list, delete_chapter):
            super().__init__()
            self.chapter = chapter
            self.rank = rank
            self.questions_list = questions_list
            self.delete_chapter = delete_chapter

        def build(self):
            self.annotation = ft.Text(f"Раздел {self.rank}:", width=150, size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
            self.chapter_name = ft.TextField(value= self.chapter.text, text_style=SubHeadlineStyle, width=765, border=ft.InputBorder.UNDERLINE)
            self.button_delete = ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color="pink600", icon_size=30, tooltip="Удалить раздел", on_click=self.delete_self)
            self.questions = ft.Column([RenderedQuestion(num, question.text, question.is_obligatory, self.delete_question) for num, question in enumerate(self.questions_list, start=1)])
            self.button_add_question = ft.ElevatedButton("Добавить вопрос", icon="add", data=str(self.rank)+' question', on_click=self.add_question)
            self.divider = ft.Divider(thickness=1)
            self.chapter_name_row = ft.Row(controls=[self.annotation, self.chapter_name, self.button_delete], width=1000)
            self.final_column = ft.Column([self.chapter_name_row, self.questions, self.button_add_question, self.divider])
            return self.final_column
        
        def add_question(self, e):
            num = len(self.questions.controls)+1
            self.questions.controls.append(RenderedQuestion(num,"",0, self.delete_question))
            self.update()

        def delete_question(self, question):
            self.questions.controls.remove(question)
            for num, question in enumerate(self.questions.controls): #не работает, видимо надо выносить номера из вопросов наружу
                question.update_rank(num)
            self.update()
        
        def delete_self(self, e):
            self.delete_chapter(self)


    class RenderedQuestionnaire(ft.UserControl):

        def __init__(self, questionnaire_elements):
            super().__init__()
            self.initial_questionnaire = questionnaire_elements['questionnaire']
            self.questionnaire = Questionnaire(name = self.initial_questionnaire.name, 
                                               version = self.initial_questionnaire.version, 
                                               author = self.initial_questionnaire.author,
                                               id_chapters_string = self.initial_questionnaire.id_chapters)
            self.raw_chapters = questionnaire_elements['chapters']
            self.questionnaire.set_id_chapters([x.id for x in self.raw_chapters.keys()])
            #print(self.questionnaire.id_chapters)
            #self.name_text = self.questionnaire.name

        def build(self):    
            self.name = ft.TextField(value=self.questionnaire.name, width=900, text_style=HeadlineStyle, border=ft.InputBorder.UNDERLINE, disabled = True, on_change=self.name_changed)
            self.chapters = ft.Column([RenderedChapter(chapter, 1, questions, self.delete_chapter) for chapter, questions in self.raw_chapters.items()], disabled=True) #rank
            self.button_add_chapter = ft.ElevatedButton("Добавить раздел", icon="add", on_click=self.add_chapter, disabled=True)
            self.button_allow_edit = ft.FilledButton("Редактировать", icon="edit", on_click=self.allow_edit)
            self.button_cancel_edit = ft.FilledButton("Отменить", icon="edit_off", visible=False, on_click=self.cancel_edit)
            self.button_save_edit = ft.FilledButton("Сохранить", icon="save", visible=False, on_click=self.save_edit)
            self.edit_control_row = ft.Row([self.button_allow_edit, self.button_cancel_edit, self.button_save_edit])
            self.final_column = ft.Column([self.name, self.edit_control_row, self.chapters, self.button_add_chapter], scroll=ft.ScrollMode.AUTO)
            return self.final_column 
        
        def name_changed(self, e):
            self.questionnaire.name = e.control.value
            self.update()
        
        # Добавление / удаление элементов
        
        def add_chapter(self, e):
            
            empty_chapter = Chapter(text='', 
                              id_questions_string = list_to_string2([])
                              )
            questions = [] 
            self.chapters.controls.append(RenderedChapter(empty_chapter, 1, questions, self.delete_chapter))
            self.update()

        def delete_chapter(self, chapter):
            self.chapters.controls.remove(chapter)
            self.update()

        # Редактирование

        def allow_edit(self, e):
            self.name.disabled = False
            self.chapters.disabled = False
            self.button_add_chapter.disabled = False
            self.button_allow_edit.visible = False
            self.button_cancel_edit.visible = True
            self.button_save_edit.visible = True
            self.update()

        def cancel_edit(self, e):
            self.name.disabled = True
            self.chapters.disabled = True
            self.button_add_chapter.disabled = True
            self.button_allow_edit.visible = True
            self.button_cancel_edit.visible = False
            self.button_save_edit.visible = False
            #self.chapters = ft.Column([RenderedChapter(chapter, questions, self.delete_chapter) for chapter, questions in self.raw_chapters.items()], disabled=True)
            self.update()
        
        def save_edit(self, e):
            self.questionnaire.set_id_chapters([x.chapter.id for x in self.chapters.controls])
            print(self.questionnaire.id_chapters)
            #Баг - если изменить название в новом опроснике несколько раз, сохраняется только последняя версия, если вернуть в исходному названию - выдается ошибка при сохранении.
            #наверное можно пересоздавать весь Questionnaire при сохранении, это самый просто вариант
            if hash_id([self.questionnaire.name, self.questionnaire.version, self.questionnaire.id_chapters]) == self.initial_questionnaire.id:
                print("Опросник существует") #прикрутить окно с предупреждением
            else:
                if self.questionnaire.name == self.initial_questionnaire.name: 
                    self.questionnaire.version += 1
                    self.initial_questionnaire.id_succesor = self.questionnaire.id
                    db.commit()
                    print('OK here')
                else:
                    self.questionnaire.version = 1
                
                self.questionnaire.update_id()
                db.add_questionnaire(self.questionnaire)
            
            self.name.disabled = True
            self.chapters.disabled = True
            self.button_add_chapter.disabled = True
            self.button_allow_edit.visible = True
            self.button_cancel_edit.visible = False
            self.button_save_edit.visible = False
            self.update()

 
    db = DataBase(db_name=DATABASE_URL)

    tables_select = db.select_questionnaries_table()

    questionnaire_select = db.select_questionnaire_by_id("25e668673bb3dc86edd0f98b186423bfa1d2aeba0a476c408928a360")


 
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Все опросники",
                icon=ft.icons.TABLE_CHART,
                content= RenderedQuestionnairesTable(tables_select), #RenderedTable
            ),
            ft.Tab(
                text="Редактирование",
                icon=ft.icons.EDIT_DOCUMENT,
                content=RenderedQuestionnaire(questionnaire_select),
            ),
        ],
        expand=1,
    )


    #вьюха
    view_questionnaires = ft.View("/questionnaires",
                [
                    bar,
                    ft.Row([rail, ft.VerticalDivider(width=1), tabs], expand=True),
                ],
            )
    
    return view_questionnaires