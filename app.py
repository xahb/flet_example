import flet as ft

from common_elements import Bar, Rail
from views import ViewMain, ViewModels, ViewValidations, ViewQuestionnaires, ViewNewValidation


def main(page: ft.Page):

    routes_keys = ['/', 
                  '/models',
                  '/validations',
                  '/questionnaires',
                  '/new_validation']
    
    rail = Rail(page, routes_keys) #немного неуместно тут стоит генерация рейла, но ему нужны ключи
    
    routes_values = [ViewMain(Bar("Главная"), rail),
                     ViewModels(Bar("Реестр моделей"), rail),
                     ViewValidations(Bar("Реестр валидаций"), rail),
                     ViewQuestionnaires(Bar("Реестр опросников"), rail),
                     ViewNewValidation(Bar("Новая валидация"), rail)
                     ]
    
    routes = dict(zip(routes_keys, routes_values))
    
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