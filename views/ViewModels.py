import flet as ft

def ViewModels(bar, rail):

    view_models = ft.View("/models",
                [
                    bar,
                    ft.Row([rail, ft.VerticalDivider(width=1), ft.Text("Тут будет список моделей")], expand=True),
                ],
            )
    
    return view_models