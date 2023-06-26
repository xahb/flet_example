import flet as ft

def ViewValidations(bar, rail):

    view_Validations = ft.View("/validations",
                [
                    bar,
                    ft.Row([rail, ft.VerticalDivider(width=1), ft.Text("Тут будет список валидаций")], expand=True),
                ],
            )
    
    return view_Validations