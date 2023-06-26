import flet as ft

def ViewMain(bar, rail):

    view_main = ft.View("/",
                [
                    bar,
                    ft.Row([rail, ft.VerticalDivider(width=1), ft.Text("Тут будет дэшборд")], expand=True),
                ],
            )
    
    return view_main