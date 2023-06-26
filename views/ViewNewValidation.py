import flet as ft
from misc import questionnaire

def ViewNewValidation(bar, rail):

    #опросник
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

    rendered_questionnaire = ft.Column(questionnaire_elements)


    view_New_Validation = ft.View("/new_validation",
                [
                    bar,
                    ft.Row([rail, ft.VerticalDivider(width=1), rendered_questionnaire], expand=True),
                ],
            )
    
    return view_New_Validation