import flet as ft
from misc import questionnaire

def main(page: ft.Page):

    #верхняя панель
    app_icon = ft.Icon(name=ft.icons.FAVORITE, color=ft.colors.PINK)
    def build_bar(title):
        return ft.AppBar(leading=app_icon, title=ft.Text(title))

    #боковая панель (навигация)
    def rail_changed(e):
        page.go(list(routes.keys())[e.control.selected_index]) #Маппинг по индексу как-то тупо, но я не нашел как в рейле сделать лучше

    rail = ft.NavigationRail(
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, 
                                        text="Новая валидация", 
                                        on_click=lambda _: page.go("/new_validation")),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.SPACE_DASHBOARD_OUTLINED, 
                selected_icon=ft.icons.SPACE_DASHBOARD, 
                label="Дэшборд"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SCREEN_SEARCH_DESKTOP_OUTLINED, 
                selected_icon=ft.icons.SCREEN_SEARCH_DESKTOP, 
                label="Модели"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.INSIGHTS_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.INSIGHTS),
                label="Валидации",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CHECKLIST_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.CHECKLIST),
                label_content=ft.Text("Опросники"),
            ),],
        on_change=rail_changed
    )

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


    #вьюхи
    
    view_main = ft.View("/",
                [
                    build_bar("Дэшборд"),
                    ft.Row([rail, ft.VerticalDivider(width=1), ft.Text("Тут будет дэшборд")], expand=True),
                ],
            )
    
    view_models = ft.View("/models",
                [
                    build_bar("Реестр моделей"),
                    ft.Row([rail, ft.VerticalDivider(width=1), ft.Text("Тут будет список моделек")], expand=True),
                ],
            )
    
    view_validations = ft.View("/validations",
                [
                    build_bar("Реестр валидаций"),
                    ft.Row([rail, ft.VerticalDivider(width=1), ft.Text("Тут будет список валидаций")], expand=True),
                ],
            )
    
    view_questionnaires = ft.View("/questionnaires",
                [
                    build_bar("Реестр опросников"),
                    ft.Row([rail, ft.VerticalDivider(width=1), ft.Text("Тут будет список опросников")], expand=True),
                ],
            )
    
    view_new_validation = ft.View("/new_validation",
                [
                    build_bar("Новая валидация"),
                    ft.Row([rail, ft.VerticalDivider(width=1), rendered_questionnaire], expand=True),
                ],
            )
    
    routes = {
        '/':view_main,
        '/models':view_models,
        '/validations':view_validations,
        '/questionnaires':view_questionnaires,
        '/new_validation':view_new_validation,
    }

    #роутинг
    def route_change(route):
        page.views.clear()
        page.views.append(routes.get(page.route))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)    


ft.app(target=main)