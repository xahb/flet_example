import flet as ft

#верхняя панель
app_icon = ft.Icon(name=ft.icons.FAVORITE, color=ft.colors.PINK)
def Bar(title):
    return ft.AppBar(leading=app_icon, title=ft.Text(title))

#боковая панель (навигация)
def Rail(page, routes_keys):

    def rail_changed(e):
        page.go(routes_keys[e.control.selected_index]) #Маппинг по индексу как-то тупо, но я не нашел как в рейле сделать лучше
        #page и routes находятся в app.py, функция запускается оттуда

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
    return rail