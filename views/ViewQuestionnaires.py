import flet as ft
from misc import qq


def ViewQuestionnaires(bar, rail):

    def build_table(source):
        rows = []
        for questionnaire_name, questionnaire_dict in source.items():
            for version, version_list in questionnaire_dict.items():
                rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(x)) for x in [questionnaire_name,
                                                                                        version,
                                                                                        version_list[1],
                                                                                        version_list[2]
                                                                                        ]
                        ]))

        table = ft.DataTable(
            columns = [
                ft.DataColumn(ft.Text("Опросник")),
                ft.DataColumn(ft.Text("Версия"), numeric=True),
                ft.DataColumn(ft.Text("Автор")),
                ft.DataColumn(ft.Text("Дата создания"))
            ],
            rows = rows
        )
        return table

    def build_table2(source):
        rows = []
        for questionnaire_name, questionnaire_dict in source.items():
            for version, version_list in questionnaire_dict.items():
                for chapter_rank, chapter_list in version_list[0].items():
                    for question_rank, question_list in chapter_list[1].items():
                        rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(x)) for x in [questionnaire_name,
                                                                                        version,
                                                                                        chapter_rank,
                                                                                        chapter_list[0],
                                                                                        question_rank,
                                                                                        question_list[0],
                                                                                        question_list[1]
                                                                                        ]
                        ]))

        table = ft.DataTable(
            columns = [
                ft.DataColumn(ft.Text("Опросник")),
                ft.DataColumn(ft.Text("Версия"), numeric=True),
                ft.DataColumn(ft.Text("Номер раздела"), numeric=True),
                ft.DataColumn(ft.Text("Название раздела")),
                ft.DataColumn(ft.Text("Номер вопроса"), numeric=True),
                ft.DataColumn(ft.Text("Текст вопроса")),
                ft.DataColumn(ft.Text("Обязательное поле"))
            ],
            rows = rows
        )
        return table

    view_questionnaires = ft.View("/questionnaires",
                [
                    bar,
                    ft.Row([rail, ft.VerticalDivider(width=1), build_table(qq)], expand=True),
                ],
            )
    
    return view_questionnaires