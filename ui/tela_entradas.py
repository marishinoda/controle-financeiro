import flet as ft
from datetime import datetime
from data.gastos_repo import adicionar_entrada, excluir_entrada, buscar_entradas
from data.gastos_repo import adicionar_entrada, excluir_entrada, buscar_entradas, converter_real_para_float

from ui.layout_base import (
    CARD_BG,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
    CARD_RADIUS,
    CARD_PADDING,
)

def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def tela_entradas(page: ft.Page, navegar):
    entradas = buscar_entradas()

    # Campos
    descricao = ft.TextField(
        label="Descrição",
        hint_text="Ex: Salário, Pix, Freelance",
        filled=True,
        bgcolor="#ffffff",
        border_radius=25,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    valor = ft.TextField(
        label="Valor",
        hint_text="R$ 0,00",
        keyboard_type=ft.KeyboardType.NUMBER,
        filled=True,
        bgcolor="#ffffff",
        border_radius=25,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    data = ft.TextField(
        label="Data",
        value=datetime.now().strftime("%d/%m/%Y"),
        filled=True,
        bgcolor="#ffffff",
        border_radius=25,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    # Função salvar
    def salvar_entrada(e):
        try:
            descricao_valor = descricao.value
            valor_valor = converter_real_para_float(valor.value)
            data_valor = datetime.strptime(data.value, "%d/%m/%Y").strftime("%Y-%m-%d")

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
                bgcolor="#e75480",
                border_radius=25,
                content=ft.Row(
                    controls=[
                        ft.Text(
                            "Salvar entrada",
                            color="white",
                            weight=ft.FontWeight.BOLD,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                on_click=salvar_entrada,
            ),

            ft.Container(height=10),

            *[

                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            f"{item['descricao']} - {formatar_real(float(item['valor']))}",
                            size=18,
                            weight=ft.FontWeight.W_500,
                            color=TEXT_PRIMARY,
                        ),

                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="red",
                            tooltip="Excluir",
                            on_click=lambda e, item=item: excluir(item, page, navegar)
                        ),
                    ]
                )

                for item in entradas
            ],

            # Voltar
            ft.TextButton(
                content=ft.Text("← Voltar", color=TEXT_SECONDARY),
                on_click=lambda e: navegar("home"),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=14,
    )

def excluir(item, page, navegar):

    excluir_entrada(item["id"])

    page.snack_bar = ft.SnackBar(
        ft.Text("Entrada excluída"),
        open=True
    )

    navegar("entradas")