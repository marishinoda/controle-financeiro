import flet as ft
from datetime import datetime
from data.gastos_repo import adicionar_entrada

from ui.layout_base import (
    CARD_BG,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
    CARD_RADIUS,
    CARD_PADDING,
)


def tela_entradas(page: ft.Page, navegar):

    # Campos
    descricao = ft.TextField(
        label="Descrição",
        hint_text="Ex: Salário, Pix, Freelance",
        filled=True,
        bgcolor=CARD_BG,
        border_radius=CARD_RADIUS,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    valor = ft.TextField(
        label="Valor",
        hint_text="R$ 0,00",
        keyboard_type=ft.KeyboardType.NUMBER,
        filled=True,
        bgcolor=CARD_BG,
        border_radius=CARD_RADIUS,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    data = ft.TextField(
        label="Data",
        value=datetime.now().strftime("%d/%m/%Y"),
        filled=True,
        bgcolor=CARD_BG,
        border_radius=CARD_RADIUS,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    # Função salvar
    def salvar_entrada(e):
        try:
            descricao_valor = descricao.value
            valor_valor = float(valor.value.replace(",", "."))
            data_valor = data.value

            adicionar_entrada(descricao_valor, valor_valor, data_valor)

            print("Entrada salva com sucesso!")

            # limpar campos
            descricao.value = ""
            valor.value = ""

            page.update()

        except Exception as erro:
            print("Erro ao salvar entrada:", erro)

    return ft.Column(
        controls=[
            # Título
            ft.Text(
                "Entradas",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
            ),

            ft.Container(height=20),

            descricao,
            valor,
            data,

            ft.Container(height=20),

            # Botão salvar
            ft.Container(
                width=240,
                height=50,
                bgcolor=ACCENT,
                border_radius=25,
                content=ft.Row(
                    controls=[
                        ft.Text(
                            "Salvar entrada",
                            color=ft.Colors.BLACK,
                            weight=ft.FontWeight.BOLD,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                on_click=salvar_entrada,
            ),

            ft.Container(height=10),

            # Voltar
            ft.TextButton(
                content=ft.Text("← Voltar", color=TEXT_SECONDARY),
                on_click=lambda e: navegar("home"),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=14,
    )