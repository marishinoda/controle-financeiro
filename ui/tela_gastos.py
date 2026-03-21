import flet as ft
from datetime import datetime

from data.gastos_repo import adicionar_gasto

from ui.layout_base import (
    CARD_BG,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
    CARD_RADIUS,
)


def tela_gastos(page: ft.Page, navegar):

    # Campos
    descricao = ft.TextField(
        label="Descrição",
        hint_text="Ex: Aluguel, Mercado, Internet",
        filled=True,
        bgcolor=CARD_BG,
        border_radius=CARD_RADIUS,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    valor = ft.TextField(
        label="Valor",
        hint_text="R$ 0,00",
        filled=True,
        bgcolor=CARD_BG,
        border_radius=CARD_RADIUS,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        on_change=lambda e: atualizar_valor(e),
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

    def formatar_digito(valor_str):
        numeros = "".join(filter(str.isdigit, valor_str))

        if numeros == "":
            return "R$ 0,00"

        valor = int(numeros) / 100

        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def atualizar_valor(e):
        e.control.value = formatar_digito(e.control.value)
        e.control.update()

    def salvar_gasto(e):
        try:
            descricao_valor = descricao.value
            valor_valor = float(valor.value.replace(",", "."))
            data_valor = datetime.strptime(data.value, "%d/%m/%Y").strftime("%Y-%m-%d")

            adicionar_gasto(descricao_valor, valor_valor, data_valor)

            print("Gasto salvo com sucesso!")

            # limpa campos
            descricao.value = ""
            valor.value = ""
            page.update()

        except Exception as erro:
            print("Erro ao salvar gasto:", erro)

    return ft.Column(
        controls=[
            # Título
            ft.Text(
                "Gastos", 
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
                            "Salvar gasto",
                            color=ft.Colors.BLACK,
                            weight=ft.FontWeight.BOLD,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                on_click=salvar_gasto,
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