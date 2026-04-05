import flet as ft

from data.anotacoes_repo import buscar_anotacao, salvar_anotacao


def tela_anotacoes(page: ft.Page, navegar, mes_atual):
    ano = mes_atual["ano"]
    mes = mes_atual["mes"]

    anotacao = buscar_anotacao(ano, mes)

    campo_texto = ft.TextField(
        multiline=True,
        min_lines=12,
        max_lines=18,
        border_radius=20,
        color="#666666",
        hint_style=ft.TextStyle(color="#999999"),
        value=anotacao["texto"] if anotacao else "",
        hint_text="Escreva suas metas, lembretes ou observações do mês...",
    )

    def salvar(e):
        salvar_anotacao(ano, mes, campo_texto.value)

        page.snack_bar = ft.SnackBar(
            ft.Text("Anotação salva ✨"),
            open=True,
        )
        page.update()

    return ft.Container(
        bgcolor="#f5e6ea",
        padding=20,
        expand=True,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text(
                    f"📝 Anotações • {mes}/{ano}",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#555555",
                ),
                ft.Container(
                    bgcolor="white",
                    border_radius=30,
                    padding=20,
                    content=campo_texto,
                ),

                ft.Container(
                    width=float("inf"),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                        controls=[
                            ft.Container(
                                width=120,
                                height=44,
                                bgcolor="#eb5c8c",
                                border_radius=30,
                                alignment=ft.Alignment(0, 0),
                                on_click=salvar,
                                content=ft.Text(
                                    "Salvar",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                ),
                            ),

                            ft.Container(
                                bgcolor="#f3e8ed",
                                border_radius=30,
                                padding=ft.padding.symmetric(horizontal=24, vertical=12),
                                on_click=lambda e: navegar("home"),
                                content=ft.Row(
                                    tight=True,
                                    spacing=8,
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.ARROW_BACK,
                                            color="#6b6b6b",
                                        ),
                                        ft.Text(
                                            "Voltar",
                                            size=16,
                                            weight=ft.FontWeight.W_600,
                                            color="#6b6b6b",
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            ]
        ),
    )








