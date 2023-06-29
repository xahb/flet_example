import flet as ft
from misc import qq

#опросник
def RenderedQuestionnaire(questionnaire):

    questionnaire_elements = []

    for ch_num, chapter in questionnaire.items():
        
        ch_text = ft.Text(f"{ch_num}. {chapter[0]}:", style=ft.TextThemeStyle.HEADLINE_SMALL)
        questionnaire_elements.append(ch_text)
        
        for q_num, question in chapter[1].items():
            q_text = ft.Text(f"{ch_num}.{q_num}. {question[0]}:", max_lines=5, width=600)
            q_answer = ft.TextField(multiline=True, filled=True, label="Комментарий", width=600)
            q_grade = ft.Dropdown(width=300, options=[ft.dropdown.Option("Красный"), ft.dropdown.Option("Желтый"), ft.dropdown.Option("Зеленый"), ft.dropdown.Option("Не оценивается")], label="Цвет оценки")
            row = ft.Row(controls=[q_text, q_answer, q_grade], wrap=True)
            questionnaire_elements.append(row)

        questionnaire_elements.append(ft.Divider(thickness=1))

    return ft.Column(questionnaire_elements, scroll=ft.ScrollMode.AUTO)


def QuestionnaireSelector(source):

    def selector_changed():
        pass

    questionnaires_list = []   
    for questionnaire_name, questionnaire_dict in source.items():
        for version, version_list in questionnaire_dict.items():
            questionnaires_list.append(f"{questionnaire_name} - вер. {version}")

    return ft.Dropdown(options=[ft.dropdown.Option(x) for x in questionnaires_list], on_change=selector_changed)


def ViewNewValidation(bar, rail):

    questionnaire = qq['Нормальный опросник'][1][0]
    main_column = ft.Column(controls=[QuestionnaireSelector(qq), RenderedQuestionnaire(questionnaire)], scroll=ft.ScrollMode.AUTO)

    view_New_Validation = ft.View("/new_validation",
                [
                    bar,
                    ft.Row([rail, 
                            ft.VerticalDivider(width=1),
                            main_column
                            ], expand=True),
                ],
            )
    
    return view_New_Validation