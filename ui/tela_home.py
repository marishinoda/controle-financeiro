import flet as ft
from datetime import datetime

from ui.layout_base import (
    CARD_BG,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
    CARD_RADIUS,
    CARD_PADDING,
)


def mes_formatado(mes_atual):
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return f"{meses[mes_atual['mes'] - 1]} {mes_atual['ano']}"

def card_home(page, titulo, subtitulo, on_click):


    return ft.Container(
        width=300,
        height=120,
        bgcolor=CARD_BG,
        border_radius=CARD_RADIUS,
        padding=CARD_PADDING,
        on_click=on_click,
        content=ft.Column(
            spacing=6,
            controls=[
                ft.Text(
                    titulo,
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ACCENT,
                ),
                ft.Text(
                    subtitulo,
                    size=14,
                    color=TEXT_SECONDARY,
                ),
            ],
        ),
    )


def tela_home(page: ft.Page, navegar, mes_atual):
    return ft.Column(
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            # Título
            ft.Text(
                "Controle Financeiro",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
            ),

            # Mês com setinhas
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.CHEVRON_LEFT,
                        icon_color=ACCENT,
                        on_click=lambda e: navegar("home", -1),
                    ),
                    ft.Text(
                        mes_formatado(mes_atual),
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ACCENT,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CHEVRON_RIGHT,
                        icon_color=ACCENT,
                        on_click=lambda e: navegar("home", 1),
                    ),
                ],
            ),

            ft.Container(height=10),

            # Cards
            card_home(
                page,
                "Entradas",
                "Adicionar valores recebidos",
                lambda e: navegar("entradas"),
            ),

            card_home(
                page,
                "Gastos",
                "Controlar despesas",
                lambda e: navegar("gastos"),
            ),

            card_home(
                page,
                "Planejamento",
                "O que pagar no mês",
                lambda e: navegar("planejamento"),
            ),
        ],
    )
