import flet as ft

from common_elements import Bar, Rail
from views import ViewMain, ViewModels, ViewValidations, ViewQuestionnaires, ViewNewValidation

from sqlalchemy import create_engine
from sqlalchemy import func
from model import Questionnaire, Base

#from misc import DATABASE_URL

#engine = create_engine(DATABASE_URL)

# Создание таблицы
#Base.metadata.create_all(engine) 

#from sqlalchemy.orm import sessionmaker
#Session = sessionmaker(bind=engine)



def main(page: ft.Page):

    theme = ft.Theme()
    theme.page_transitions.android = ft.PageTransitionTheme.OPEN_UPWARDS
    theme.page_transitions.ios = ft.PageTransitionTheme.CUPERTINO
    theme.page_transitions.macos = ft.PageTransitionTheme.FADE_UPWARDS
    theme.page_transitions.linux = ft.PageTransitionTheme.ZOOM
    theme.page_transitions.windows = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.update()

    routes_keys = ['/', 
                  '/models',
                  '/validations',
                  '/questionnaires',
                  '/new_validation']
    
    rail = Rail(page, routes_keys) #немного неуместно тут стоит генерация рейла, но ему нужны ключи
    
    routes_values = [ViewMain(Bar("Главная"), rail),
                     ViewModels(Bar("Реестр моделей"), rail),
                     ViewValidations(Bar("Реестр валидаций"), rail),
                     ViewQuestionnaires(page, Bar("Реестр опросников"), rail),
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
#ft.app(target=main, view=ft.WEB_BROWSER)