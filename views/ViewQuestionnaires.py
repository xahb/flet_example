import flet as ft
from misc import qq


def ViewQuestionnaires(page, bar, rail):

    def RenderedTable(source):
        rows = []
        for questionnaire_name, questionnaire_dict in source.items():
            for version, version_list in questionnaire_dict.items():
                rows.append(ft.DataRow(cells=[ft.DataCell(ft.ElevatedButton(f"{questionnaire_name} - вер. {version}")),
                                              ft.DataCell(ft.Text(version_list[1])),
                                              ft.DataCell(ft.Text(version_list[2]))
                                             ]
                                      )
                           )

        table = ft.DataTable(
            columns = [
                ft.DataColumn(ft.Text("Опросник")),
                ft.DataColumn(ft.Text("Автор")),
                ft.DataColumn(ft.Text("Дата создания"))
            ],
            rows = rows
        )
        return table
    

    
    class RenderedQuestion(ft.UserControl):

        def __init__(self, number, text, obligatory):
            super().__init__()
            self.annotation = ft.Text(f"Вопрос {number}:", width=150, size=15, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
            self.text = ft.TextField(multiline=True, value= text, border=ft.InputBorder.UNDERLINE, width=600)
            self.is_obligatory = ft.Checkbox(label="Обязательный", value=obligatory, width=150)
            self.button_delete = ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color="pink600", icon_size=30, tooltip="Удалить вопрос")

        def build(self):
            return ft.Card(ft.Row(controls=[self.annotation, self.text, self.is_obligatory, self.button_delete]), width=1000)


    class RenderedChapter(ft.UserControl):

            def __init__(self, ch_num, chapter):
                super().__init__()
                self.ch_num = ch_num
                self.chapter = chapter

            def build(self):
                self.annotation = ft.Text(f"Раздел {self.ch_num}:", width=150, size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
                self.chapter_name = ft.TextField(value= self.chapter[0], text_size=18, width=765, border=ft.InputBorder.UNDERLINE)
                self.button_delete = ft.IconButton(icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color="pink600", icon_size=30, tooltip="Удалить раздел")
                self.questions = ft.Column([RenderedQuestion(q_num, question[0], question[1]) for q_num, question in self.chapter[1].items()])
                self.button_add_question = ft.ElevatedButton("Добавить вопрос", icon="add", data=str(self.ch_num)+' question', on_click=self.AddQuestion)
                self.divider = ft.Divider(thickness=1)
                self.chapter_name_row = ft.Row(controls=[self.annotation, self.chapter_name, self.button_delete], width=1000)
                self.final_column = ft.Column([self.chapter_name_row, self.questions, self.button_add_question, self.divider])
                return self.final_column
            
            def AddQuestion(self, e):
                self.questions.controls.append(RenderedQuestion(0,"",0))
                self.update()
    


    class RenderedQuestionnaire(ft.UserControl):

        def __init__(self, questionnaire):
            super().__init__()
            self.chapters = [RenderedChapter(ch_num, chapter) for ch_num, chapter in questionnaire.items()]
            self.chapters.append(ft.FilledButton("Добавить раздел", icon="add"))

        def build(self):
            return ft.Column(self.chapters, scroll=ft.ScrollMode.AUTO)

 
    questionnaire = qq['Нормальный опросник'][1][0]
 
    tabs = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Все опросники",
                icon=ft.icons.TABLE_CHART,
                content= RenderedTable(qq),
            ),
            ft.Tab(
                text="Редактирование",
                icon=ft.icons.EDIT_DOCUMENT,
                content=RenderedQuestionnaire(questionnaire),
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