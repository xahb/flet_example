import flet as ft
from misc import qq

from misc import DATABASE_URL

from model import DataBase
from model import DummyChapter
from model import DummyQuestion

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

        def __init__(self, number, text, obligatory, delete_question):
            super().__init__()
            self.annotation = ft.Text(f"Вопрос {number}:", width=150, size=15, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
            self.text = ft.TextField(multiline=True, value= text, border=ft.InputBorder.UNDERLINE, width=600)
            self.is_obligatory = ft.Checkbox(label="Обязательный", value=obligatory, width=150)
            self.button_delete = ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color="pink600", icon_size=30, tooltip="Удалить вопрос", on_click=self.delete_self)
            self.delete_question = delete_question

        def build(self):
            return ft.Card(ft.Row(controls=[self.annotation, self.text, self.is_obligatory, self.button_delete]), width=1000)
        
        def delete_self(self, e):
            self.delete_question(self)


    class RenderedChapter(ft.UserControl):

        def __init__(self, chapter, questions_list, delete_chapter):
            super().__init__()
            self.chapter = chapter
            self.questions_list = questions_list
            self.delete_chapter = delete_chapter

        def build(self):
            self.annotation = ft.Text(f"Раздел {self.chapter.id}:", width=150, size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
            self.chapter_name = ft.TextField(value= self.chapter.text, text_size=18, width=765, border=ft.InputBorder.UNDERLINE)
            self.button_delete = ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color="pink600", icon_size=30, tooltip="Удалить раздел", on_click=self.delete_self)
            self.questions = ft.Column([RenderedQuestion(question.id, question.text, question.is_obligatory, self.delete_question) for question in self.questions_list])
            self.button_add_question = ft.ElevatedButton("Добавить вопрос", icon="add", data=str(self.chapter.id)+' question', on_click=self.add_question)
            self.divider = ft.Divider(thickness=1)
            self.chapter_name_row = ft.Row(controls=[self.annotation, self.chapter_name, self.button_delete], width=1000)
            self.final_column = ft.Column([self.chapter_name_row, self.questions, self.button_add_question, self.divider])
            return self.final_column
        
        def add_question(self, e):
            self.questions.controls.append(RenderedQuestion(0,"",0, self.delete_question))
            self.update()

        def delete_question(self, question):
            self.questions.controls.remove(question)
            self.update()
        
        def delete_self(self, e):
            self.delete_chapter(self)


    class RenderedQuestionnaire(ft.UserControl):

        def __init__(self, questionnaire_elements):
            super().__init__()
            self.questionnaire = questionnaire_elements['questionnaire']
            self.raw_chapters = questionnaire_elements['chapters']
            self.name_text = "Хороший опросник"

        def build(self):
            self.name = ft.Text(self.name_text, width=900, size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT)
            self.chapters = ft.Column([RenderedChapter(chapter, questions, self.delete_chapter) for chapter, questions in self.raw_chapters.items()], disabled=True)
            self.button_add_chapter = ft.ElevatedButton("Добавить раздел", icon="add", on_click=self.add_chapter, disabled=True)
            self.button_allow_edit = ft.FilledButton("Редактировать", icon="edit", on_click=self.allow_edit)
            self.button_cancel_edit = ft.FilledButton("Отменить", icon="edit_off", visible=False, on_click=self.cancel_edit)
            self.button_save_edit = ft.FilledButton("Сохранить", icon="save", visible=False, on_click=self.save_edit)
            self.edit_control_row = ft.Row([self.button_allow_edit, self.button_cancel_edit, self.button_save_edit])
            self.final_column = ft.Column([self.name, self.edit_control_row, self.chapters, self.button_add_chapter], scroll=ft.ScrollMode.AUTO)
            return self.final_column 
        
        def add_chapter(self, e):
            questions = [DummyQuestion(0,'',0,0,0),DummyQuestion(0,'',0,0,0)]
            self.chapters.controls.append(RenderedChapter(DummyChapter(0,'',0), questions, self.delete_chapter))
            self.update()

        def delete_chapter(self, chapter):
            self.chapters.controls.remove(chapter)
            self.update()

        def allow_edit(self, e):
            self.chapters.disabled = False
            self.button_add_chapter.disabled = False
            self.button_allow_edit.visible = False
            self.button_cancel_edit.visible = True
            self.button_save_edit.visible = True
            self.update()

        def cancel_edit(self, e):
            self.chapters.disabled = True
            self.button_add_chapter.disabled = True
            self.button_allow_edit.visible = True
            self.button_cancel_edit.visible = False
            self.button_save_edit.visible = False
            self.chapters = ft.Column([RenderedChapter(chapter, questions, self.delete_chapter) for chapter, questions in self.raw_chapters.items()], disabled=True)
            self.update()
        
        def save_edit(self, e):
            pass

 
    db = DataBase(db_name=DATABASE_URL)

    tables_select = db.select_questionnaries_table()

    questionnaire_select = db.select_questionnaire_by_id(2)


 
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